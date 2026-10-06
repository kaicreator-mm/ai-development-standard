"""Sandbox-only deployed-service fixture; NO production/external provider access.

The parent test binds the exact artifact digest and sandbox environment via
explicit argv, starts this as a real separate process, and probes its health.
No registry credentials, environment mutation, or production endpoints exist.
"""
from __future__ import annotations

import hashlib
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: sandbox_service.py <published-artifact> <environment-id>", file=sys.stderr)
        return 2
    artifact = Path(sys.argv[1]).resolve(strict=True)
    environment = sys.argv[2]
    if not environment.startswith("sandbox:"):
        print("only sandbox environments are accepted", file=sys.stderr)
        return 2
    digest = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path != "/health":
                self.send_error(404)
                return
            payload = json.dumps({"environment_ref": environment, "artifact_digest": digest,
                                  "service_state": "SANDBOX_RUNNING"}, sort_keys=True).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_args: object) -> None:
            return

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        print(server.server_port, flush=True)
        server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
