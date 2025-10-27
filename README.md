# ai-executor-poc

Proof-of-concept: AI-assisted executor for **digital assets** (bank + crypto), local demo only (mock APIs).

**YamaSutra** - An  AI-powered digital will executor with divine powers

## Run locally

```bash
# create venv
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# install deps
pip install -r requirements.txt

# run app (with PYTHONPATH set to include project root)
PYTHONPATH=. python app/main.py

# Or use the startup script
./start.sh


Open http://127.0.0.1:5001 in your browser to access the YamaSutra UI

**Note:** The app runs on port 5001 instead of 5000 to avoid conflicts with macOS AirPlay Receiver.

## Features



## API Endpoints

POST /process_will — body: structured will JSON (see schema/sample_will.json). Produces proposals.

GET /proposals — list pending proposals.

POST /approve_action — approve an action; executes mock transfer and writes audit log.

GET /audit_log — returns audit log (JSON lines).

Example

Start server:

python app/main.py


Send will:

curl -X POST http://127.0.0.1:5001/process_will \
 -H "Content-Type: application/json" \
 -d @schema/sample_will.json


View proposals:

curl http://127.0.0.1:5001/proposals


Approve one:

curl -X POST http://127.0.0.1:5001/approve_action \
 -H "Content-Type: application/json" \
 -d '{"proposal_id": "p-1", "approver": "Acme Executor"}'


See audit:

curl http://127.0.0.1:5001/audit_log
