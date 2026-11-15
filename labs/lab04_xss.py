from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# UCHEBNY STEND #4 - Reflected XSS.
# Imya vstavleno v HTML bez ekranirovaniya.

FORM = "<form method=GET action=/hello><input name=name><button>OK</button></form>"

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/hello":
            name = parse_qs(u.query).get("name", [""])[0]
            # UYAZVIMO: vstavka v HTML bez ekranirovaniya
            self.send(FORM + "<h3>Privet, " + name + "!</h3>")
            return
        self.send(FORM)

if __name__ == "__main__":
    print("Stend 4 zapushchen: http://127.0.0.1:5003")
    HTTPServer(("127.0.0.1", 5003), H).serve_forever()
