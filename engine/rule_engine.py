# engine/rule_engine.py
"""
Simple rule engine: converts structured will bequests into action proposals.
Only basic logic: if 'death_confirmed' in conditions => propose action.
"""
import datetime

def _build_proposal(bequest, will_meta):
    """
    Returns a proposal dict with required fields.
    """
    asset_type = bequest.get("type")
    proposal = {
        "asset_type": asset_type,
        "bequest_id": bequest.get("id"),
        "target": bequest.get("target"),
        "beneficiary": bequest.get("beneficiary"),
        "notes": bequest.get("notes"),
        "conditions": bequest.get("conditions", []),
        "will_testator": will_meta.get("testator", {}).get("name"),
        "will_date": will_meta.get("date"),
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    # add a human-readable action suggestion
    if asset_type == "bank_account":
        proposal["suggested_action"] = f"Transfer funds per instruction ({bequest.get('notes','')}) to {proposal['beneficiary'].get('name')}"
    elif asset_type == "crypto_wallet":
        proposal["suggested_action"] = f"Send crypto holdings from {proposal['target'].get('address')} to beneficiary {proposal['beneficiary'].get('name')}"
    elif asset_type == "online_account":
        proposal["suggested_action"] = f"Archive and then close {proposal['target'].get('service')} account {proposal['target'].get('account_id')}"
    else:
        proposal["suggested_action"] = "Unknown asset type - manual review needed"
    return proposal

def generate_proposals(will_json):
    """
    Parse will JSON and create proposals for bequests meeting conditions.
    For POC we only process bequests with condition 'death_confirmed'.
    """
    proposals = []
    bequests = will_json.get("bequests", [])
    for b in bequests:
        conditions = b.get("conditions", [])
        if "death_confirmed" in conditions:
            p = _build_proposal(b, will_json)
            proposals.append(p)
    return proposals
