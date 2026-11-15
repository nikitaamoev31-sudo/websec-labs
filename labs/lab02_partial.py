import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# UCHEBNY STEND #2 - chastichnaya zashchita.
# /login zashchishchen parametrizaciey, /search - net.

def make_db():
    con = sqlite3.connect(":memory:", check_same_thread=False)
    con.execute("CREATE TABLE users(id INTEGER, login TEXT, password TEXT, secret TEXT)")
    con.executemany("INSERT INTO users VALUES (?,?,?,?)",
        [(1,"admin","SuperSecret2026","FLAG: admin_secret_key_7788"),
         (2,"nikita","qwerty","FLAG: nikita_private_data"),
         (3,"maria","12345","FLAG: maria_token_xyz")])
    con.commit()
    return con

DB = make_db()

def page(result=""):
    return "<form method=POST action=/login><input name=login><input name=password type=password><button>Voyti</button></form>" \
           "<form method=GET action=/search><input name=q><button>Iskat</button></form>" + result

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/search":
            q = parse_qs(u.query).get("q", [""])[0]
            # UYAZVIMO: sklejka stroki
            sql = "SELECT login, secret FROM users WHERE login LIKE '%" + q + "%'"
            rows = DB.execute(sql).fetchall()
            self.send(page("<pre>SQL: " + sql + "\n" + "\n".join("%s | %s" % r for r in rows) + "</pre>")); return
        self.send(page())
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        d = parse_qs(self.rfile.read(n).decode())
        login = d.get("login", [""])[0]; password = d.get("password", [""])[0]
        # ZASHCHISHCHENO: parametrizaciya
        row = DB.execute("SELECT login, secret FROM users WHERE login=? AND password=?", (login, password)).fetchone()
        self.send(page("<pre>" + ("USPEH: %s" % row[0] if row else "Login neverno (inekciya tut ne rabotaet)") + "</pre>"))

if __name__ == "__main__":
    print("Stend 2 zapushchen: http://127.0.0.1:5001")
    HTTPServer(("127.0.0.1", 5001), H).serve_forever()
