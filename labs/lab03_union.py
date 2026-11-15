import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# UCHEBNY STEND #3 - UNION-inekciya.
# Uyazvimy poisk + skrytaya tablica api_keys.

def make_db():
    con = sqlite3.connect(":memory:", check_same_thread=False)
    con.execute("CREATE TABLE users(id INTEGER, login TEXT, secret TEXT)")
    con.executemany("INSERT INTO users VALUES (?,?,?)",
        [(1,"admin","public_profile"),(2,"nikita","public_profile"),(3,"maria","public_profile")])
    con.execute("CREATE TABLE api_keys(name TEXT, token TEXT)")
    con.executemany("INSERT INTO api_keys VALUES (?,?)",
        [("stripe_live","sk_live_9931_SECRET"),("aws_root","AKIA_TOP_SECRET_42")])
    con.commit()
    return con

DB = make_db()

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())
    def do_GET(self):
        u = urlparse(self.path)
        form = "<form method=GET action=/search><input name=q><button>Iskat</button></form>"
        if u.path == "/search":
            q = parse_qs(u.query).get("q", [""])[0]
            # UYAZVIMO: sklejka stroki, 2 kolonki v vyborke
            sql = "SELECT login, secret FROM users WHERE login LIKE '%" + q + "%'"
            rows = DB.execute(sql).fetchall()
            self.send(form + "<pre>SQL: " + sql + "\n" + "\n".join("%s | %s" % r for r in rows) + "</pre>"); return
        self.send(form)

if __name__ == "__main__":
    print("Stend 3 zapushchen: http://127.0.0.1:5002")
    HTTPServer(("127.0.0.1", 5002), H).serve_forever()
