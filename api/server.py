import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import threading

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "transactions.json"

_lock = threading.Lock()

# Demo user
VALID_USERS = {"admin": "secret"}


def load_transactions():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_transactions(txs):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(txs, f, indent=2, ensure_ascii=False)


def check_auth(header: str) -> bool:
    """Check Basic Auth header."""
    if not header or not header.startswith("Basic "):
        return False
    try:
        encoded = header.split(" ", 1)[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return VALID_USERS.get(username) == password
    except Exception:
        return False


class TransactionHandler(BaseHTTPRequestHandler):
    def _send(self, code=200, data=None):
        body = b""
        if data is not None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _require_auth(self):
        if not check_auth(self.headers.get("Authorization")):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="MoMoAPI"')
            self.end_headers()
            return False
        return True

    def do_GET(self):
        if not self._require_auth():
            return

        parts = self.path.strip("/").split("/")
        txs = load_transactions()

        if self.path in ["/transactions", "/transactions/"]:
            self._send(200, txs)
        elif len(parts) == 2 and parts[0] == "transactions":
            tid = parts[1]
            tx = next((t for t in txs if str(t["id"]) == tid), None)
            if tx:
                self._send(200, tx)
            else:
                self._send(404, {"error": "Not found"})
        else:
            self._send(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if not self._require_auth():
            return
        if self.path.rstrip("/") != "/transactions":
            self._send(404, {"error": "Endpoint not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            self._send(400, {"error": "Invalid JSON"})
            return

        txs = load_transactions()
        new_id = max((int(t["id"]) for t in txs), default=0) + 1
        payload["id"] = new_id
        txs.append(payload)

        with _lock:
            save_transactions(txs)

        self._send(201, payload)

    def do_PUT(self):
        if not self._require_auth():
            return
        parts = self.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "transactions":
            tid = parts[1]
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode("utf-8"))
            except Exception:
                self._send(400, {"error": "Invalid JSON"})
                return

            txs = load_transactions()
            updated = None
            for i, tx in enumerate(txs):
                if str(tx["id"]) == tid:
                    payload["id"] = tx["id"]
                    txs[i] = payload
                    updated = payload
                    break

            if not updated:
                self._send(404, {"error": "Not found"})
                return

            with _lock:
                save_transactions(txs)

            self._send(200, updated)
        else:
            self._send(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        if not self._require_auth():
            return
        parts = self.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "transactions":
            tid = parts[1]
            txs = load_transactions()
            removed = None
            for i, tx in enumerate(txs):
                if str(tx["id"]) == tid:
                    removed = txs.pop(i)
                    break
            if not removed:
                self._send(404, {"error": "Not found"})
                return

            with _lock:
                save_transactions(txs)

            self._send(200, {"deleted": removed})
        else:
            self._send(404, {"error": "Endpoint not found"})


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), TransactionHandler)
    print("API running at http://localhost:8000 (Basic Auth: admin/secret)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()
