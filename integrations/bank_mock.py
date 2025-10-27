# integrations/bank_mock.py
"""
Simulated bank integration for POC.
This file does NOT connect to any real bank. It returns simulated responses.
"""

import uuid
import time

def simulate_bank_transfer(proposal):
    """
    Simulate bank transfer. Returns dict with success flag and details.
    """
    # pretend to contact bank, wait a little
    time.sleep(0.5)
    tx_id = "BANK-TX-" + uuid.uuid4().hex[:10]
    detail = {
        "tx_id": tx_id,
        "bank": proposal.get("target", {}).get("bank"),
        "account_id": proposal.get("target", {}).get("account_id"),
        "amount_desc": proposal.get("notes", "unspecified"),
        "timestamp": time.time()
    }
    return {"success": True, "detail": detail}
