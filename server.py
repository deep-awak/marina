import os
import subprocess
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

MARINA_BIN = "/app/marina"

PAGE_TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>marina - SAT solver</title>
  <style>
    body {{ font-family: sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; }}
    input[type=text] {{ width: 100%; padding: 8px; font-size: 1rem; box-sizing: border-box; }}
    button {{ padding: 8px 16px; margin-top: 8px; }}
    pre {{ background: #f4f4f4; padding: 12px; border-radius: 6px; white-space: pre-wrap; }}
    .error {{ color: #b00020; }}
  </style>
</head>
<body>
  <h1>marina - SAT solver</h1>
  <p>Entre une formule propositionnelle (ex: <code>(a&amp;b | c)-&gt;d &lt;-&gt; ~e</code>).</p>
  <form method="get" action="/">
    <input type="text" name="formula" value="{formula_escaped}" placeholder="(a&amp;b | c)->d <-> ~e">
    <button type="submit">Resoudre</button>
  </form>
  {result_html}
  <p><small>API: <code>GET /solve?formula=...</code> renvoie du texte brut.</small></p>
</body>
</html>
"""


def run_marina(formula: str) -> tuple[str, bool]:
    try:
        proc = subprocess.run(
            [MARINA_BIN, formula],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if proc.returncode != 0:
            return (proc.stderr.strip() or "Erreur inconnue", False)
        return (proc.stdout.strip(), True)
    except subprocess.TimeoutExpired:
        return ("Timeout: la resolution a pris trop de temps.", False)


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, body: str):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        formula = params.get("formula", [""])[0]

        if parsed.path == "/solve":
            if not formula:
                self._send(400, "text/plain; charset=utf-8", "Missing 'formula' query param")
                return
            result, ok = run_marina(formula)
            self._send(200 if ok else 400, "text/plain; charset=utf-8", result)
            return

        if parsed.path == "/healthz":
            self._send(200, "text/plain; charset=utf-8", "ok")
            return

        # root: HTML form
        result_html = ""
        if formula:
            result, ok = run_marina(formula)
            css_class = "" if ok else "error"
            result_html = f"<h2>Resultat</h2><pre class='{css_class}'>{html.escape(result)}</pre>"

        page = PAGE_TEMPLATE.format(
            formula_escaped=html.escape(formula),
            result_html=result_html,
        )
        self._send(200, "text/html; charset=utf-8", page)

    def log_message(self, format, *args):
        # Keep Render's log output clean; comment out to get verbose logs.
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Listening on 0.0.0.0:{port}")
    server.serve_forever()
