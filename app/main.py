# app/main.py
import json
import uuid
from flask import Flask, request, jsonify, render_template
from engine.rule_engine import generate_proposals
from integrations.bank_mock import simulate_bank_transfer
from integrations.crypto_mock import simulate_crypto_transfer
from utils.audit_logger import AuditLogger
import os

app = Flask(__name__)
DATA_DIR = os.path.join(os.getcwd())
PROPOSALS_FILE = os.path.join(DATA_DIR, "logs", "proposals.json")
AUDIT_LOG = os.path.join(DATA_DIR, "logs", "audit_log.jsonl")

# ensure logs folder exists
os.makedirs(os.path.join(DATA_DIR, "logs"), exist_ok=True)

# in-memory proposals cache (also persisted)
_proposals = []

def persist_proposals():
    with open(PROPOSALS_FILE, "w") as f:
        json.dump(_proposals, f, indent=2)

def load_proposals():
    global _proposals
    if os.path.exists(PROPOSALS_FILE):
        with open(PROPOSALS_FILE, "r") as f:
            try:
                _proposals = json.load(f)
            except:
                _proposals = []

load_proposals()
audit = AuditLogger(AUDIT_LOG)

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"}), 200

@app.route("/process_will", methods=["POST"])
def process_will():
    """
    Accept structured will JSON, generate proposals.
    """
    will = request.get_json()
    if not will:
        return jsonify({"error":"missing JSON body"}), 400
    proposals = generate_proposals(will)
    # assign ids and persist
    for p in proposals:
        p['proposal_id'] = "p-" + uuid.uuid4().hex[:8]
        p['status'] = 'proposed'
        _proposals.append(p)
        audit.log_event({
            "event":"proposal_created",
            "proposal_id": p['proposal_id'],
            "payload": p
        })
    persist_proposals()
    return jsonify({"status":"ok","proposals_created": len(proposals)}), 202

@app.route("/proposals", methods=["GET"])
def get_proposals():
    load_proposals()
    return jsonify({"proposals": _proposals}), 200

@app.route("/approve_action", methods=["POST"])
def approve_action():
    """
    Approve a proposal: execute mock transfer and log result.
    Body:
    {
      "proposal_id": "p-1...",
      "approver": "Name"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error":"missing JSON body"}), 400
    pid = data.get("proposal_id")
    approver = data.get("approver", "Unknown")
    load_proposals()
    matching = [p for p in _proposals if p['proposal_id'] == pid]
    if not matching:
        return jsonify({"error":"proposal not found"}), 404
    proposal = matching[0]
    if proposal['status'] != 'proposed':
        return jsonify({"error":"proposal already processed"}), 400

    # simulate execution depending on asset_type
    result = {"success": False, "detail": None}
    if proposal['asset_type'] == 'bank_account':
        result = simulate_bank_transfer(proposal)
    elif proposal['asset_type'] == 'crypto_wallet':
        result = simulate_crypto_transfer(proposal)
    elif proposal['asset_type'] == 'online_account':
        # simulate archive/close
        result = {"success": True, "detail": "account archived and closure request submitted"}
    else:
        result = {"success": False, "detail": "unknown asset type"}

    # update proposal status
    proposal['status'] = 'executed' if result.get('success') else 'failed'
    proposal['executed_by'] = approver
    proposal['execution_result'] = result
    persist_proposals()

    # log to audit
    audit.log_event({
        "event": "proposal_executed",
        "proposal_id": pid,
        "approver": approver,
        "result": result
    })

    return jsonify({"status": proposal['status'], "result": result}), 200

@app.route("/audit_log", methods=["GET"])
def get_audit():
    logs = audit.read_all()
    return jsonify({"audit": logs}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
