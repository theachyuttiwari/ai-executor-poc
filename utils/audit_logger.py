# utils/audit_logger.py
import json
import hashlib
import time
from pathlib import Path

class AuditLogger:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.filepath.touch()

    def _hash_payload(self, payload):
        s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def log_event(self, payload):
        entry = {
            "timestamp": time.time(),
            "payload": payload,
        }
        entry["payload_hash"] = self._hash_payload(entry["payload"])
        line = json.dumps(entry)
        with open(self.filepath, "a") as f:
            f.write(line + "\n")
        return entry

    def read_all(self):
        lines = []
        with open(self.filepath, "r") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    lines.append(json.loads(ln))
                except:
                    continue
        return lines
