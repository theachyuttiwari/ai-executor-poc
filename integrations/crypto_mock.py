# integrations/crypto_mock.py
"""
Simulated crypto integration for POC.
No real blockchain calls. Returns a fake transaction hash.
"""

import uuid
import time

def simulate_crypto_transfer(proposal):
    time.sleep(0.5)
    fake_tx = "0x" + uuid.uuid4().hex*2
    detail = {
        "tx_hash": fake_tx[:66],
        "chain": proposal.get("target", {}).get("chain"),
        "from_address": proposal.get("target", {}).get("address"),
        "to_beneficiary": proposal.get("beneficiary", {}).get("name"),
        "notes": proposal.get("notes"),
        "timestamp": time.time()
    }
    return {"success": True, "detail": detail}
