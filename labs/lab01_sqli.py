import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# UCHEBNY STEND #1 - SQL-inekciya v forme logina.
# Namerenno uyazvimy kod. Zapuskat TOLKO lokalno.

def make_db():
    con = sqlite3.connect(":memory:", check_same_thread=False)
    con.execute("CREATE TABLE users(id INTEGER, login TEXT, password TEXT, secret TEXT)")
    con.executemany(
        "INSERT INTO users VALUES (?,?,?,?)",
        [(1, "admin", "SuperSecret2026", "FLAG: admin_panel_access"),
         (2, "nikita", "qwerty", "FLAG: user_data_leak")],
    )
    con.commit()
    return con

DB = make_db()

PAGE = """<!doctype html><html lang=ru><meta charset=utf-8>
<title>Lab 01</title>
<form method=POST>
<input name=login placeholder=Login>
<input name=password placeholder=Parol type=password>
<button>Voyti</button>
</form>
{result}
</html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
    def do_GET(self):
        self._send(PAGE.format(result=""))
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        data = parse_qs(self.rfile.read(n).decode("utf-8"))
        login = data.get("login", [""])[0]
        password = data.get("password", [""])[0]
        # UYAZVIMOST: sklejka stroki
        query = "SELECT login, secret FROM users WHERE login = '%s' AND password = '%s'" % (login, password)
        box = "<div>SQL: " + query + "<br>"
        try:
            row = DB.execute(query).fetchone()
            box += ("USPEH! Voshli kak: %s %s" % (row[0], row[1])) if row else "Neverny login ili parol"
        except Exception as e:
            box += "Oshibka SQL: %s" % e
        box += "</div>"
        self._send(PAGE.format(result=box))

if __name__ == "__main__":
    print("Stend zapushchen: http://127.0.0.1:5000")
    HTTPServer(("127.0.0.1", 5000), H).serve_forever()
