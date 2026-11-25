import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Policy hierarchy
p = Fig(1100, 520, "The policy hierarchy: why, what exactly, in what flow, how step by step, and what is advised",
        "A pyramid. Policy at the top states management's intent and why, technology-neutral and long-lived. A standard sets specific, "
        "mandatory, measurable requirements, such as AES-256-GCM for Confidential data. A process sets the flow of work: activities, "
        "order, owners, inputs, and outputs. A procedure gives the exact steps. Beside it, a guideline offers recommended but "
        "optional practice. Higher levels change slowly; lower levels change often.")
lv = [("Policy", "why: management's intent; long-lived", "certificate", "#1f4e9c"), ("Standard", "what exactly: mandatory and measurable,\ne.g. AES-256-GCM for Confidential data", "checklist", "#2471a3"),
      ("Process", "the flow of work: activities, order,\nowners, inputs, outputs", "nodes", "#2e86c1"), ("Procedure", "how, step by step", "logbook", "#5dade2")]
for i, (name, sub, ic, col) in enumerate(lv):
    y = 70 + i * 100; top = 120 + i * 90; bot = 120 + (i + 1) * 90
    p.poly([(400 - top / 2 + 40, y), (400 + top / 2 - 40, y), (400 + bot / 2 - 40, y + 94), (400 - bot / 2 + 40, y + 94)], col, "#ffffff", 2, step=i + 1)
    p.icon(ic, 400, y + 46, 46, step=i + 1)
    p.raw(f'<line x1="{400 + bot / 2 - 30:.0f}" y1="{y + 47}" x2="660" y2="{y + 47}" stroke="#9aa5b1" stroke-dasharray="4 4"/>', step=i + 1)
    p.text(670, y + 40, name, 17, col, "bold", "start", step=i + 1); p.text(670, y + 60, sub, 13, INK, anchor="start", step=i + 1)
    p.badge(i + 1, 640, y + 47, step=i + 1, color=col)
p.card(40, 180, 170, 170, "search", "Guideline", "recommended,\nnot mandatory", "#7f8c8d", step=5, icon_size=50, title_size=16); p.badge(5, 50, 190, step=5, color="#7f8c8d")
p.arrow([(1060, 90), (1060, 450)], None, MUTED, step=6, width=2.2); p.text(1050, 476, "changes more often", 12, MUTED, "bold", "end", step=6)
p.text(1050, 76, "changes rarely", 12, MUTED, "bold", "end", step=6)
p.save(OUT + "ch19_policy_pyramid")

# Board reporting
b = Fig(1100, 480, "Board reporting: translate technical metrics into business outcomes",
        "Left: a technical statement such as the number of vulnerabilities patched this month means little to a board. Right: the "
        "same work stated as an outcome: mean time to patch critical vulnerabilities fell from 21 to 7 days, cutting the exposure "
        "window by 66 percent. Below, common board metrics: mean time to detect, mean time to respond, patch compliance, phishing "
        "click rate, open critical findings, third-party coverage, and audit closure.")
b.rect(30, 60, 400, 180, "#f4f6f8", "#9aa5b1", 1.6, rx=10, step=1); b.icon("checklist", 80, 150, 60, step=1)
b.text(260, 130, "Number of vulnerabilities", 16, INK, "bold", step=1); b.text(260, 154, "patched this month", 16, INK, "bold", step=1)
b.text(260, 196, "a count without a business meaning", 13, RED, "bold", step=1); b.badge(1, 30, 60, step=1, color=RED)
b.arrow([(436, 150), (520, 150)], "translate", BLUE, step=2, size=13, width=3)
b.rect(530, 60, 540, 180, "#eef5fc", BLUE, 2, rx=10, step=2); b.icon("group", 590, 150, 70, step=2)
b.text(820, 110, "Mean time to patch critical", 16, INK, "bold", step=2)
b.text(780, 150, "21 days", 26, RED, "bold", step=3); b.arrow([(840, 142), (890, 142)], None, GREEN, step=3, width=3); b.text(940, 150, "7 days", 26, GREEN, "bold", step=3)
b.text(820, 196, "exposure window cut by 66 percent", 15, GREEN, "bold", step=3); b.badge(2, 530, 60, step=2); b.badge(3, 1050, 120, step=3, color=GREEN)
mets = [("clock", "MTTD"), ("gear", "MTTR"), ("check", "Patch compliance"), ("envelope", "Phishing click rate"), ("bug", "Open critical findings"), ("nodes", "Third-party coverage"), ("logbook", "Audit closure")]
for i, (ic, lab) in enumerate(mets):
    x = 80 + i * 150; b.icon(ic, x, 330, 44, step=4); b.text(x, 380, lab, 12, INK, "bold", step=4)
b.badge(4, 30, 300, step=4)
b.text(550, 440, "Pair them with key risk indicators, which warn before an incident rather than after.", 13, MUTED, italic=True, step=5)
b.save(OUT + "ch19_board_reporting")

# Three lines model
t = Fig(1100, 520, "The three lines model: who owns, who challenges, who assures",
        "The board and its audit committee hold accountability and oversight. Executive management directs the first line, which owns "
        "and operates controls, such as engineering, IT operations, and application teams, and the second line, which sets policy, "
        "monitors, and challenges, such as security, risk, and compliance. The third line, internal audit, provides independent "
        "assurance and reports to the audit committee rather than to management.")
t.card(380, 50, 340, 110, "bank", "Board and audit committee", "accountability and oversight", "#2b3138", step=1, icon_size=44, title_size=15)
t.card(150, 210, 320, 100, "group", "Executive management", "directs and resources", BLUE, step=2, icon_size=40, title_size=15)
t.card(30, 360, 300, 140, "gear", "First line", "owns and operates controls:\nengineering, IT ops, app teams", "#16a085", step=3, icon_size=44, title_size=16)
t.card(410, 360, 300, 140, "eye", "Second line", "sets policy, monitors, challenges:\nsecurity, risk, compliance", ORANGE, step=4, icon_size=44, title_size=16)
t.card(760, 260, 310, 140, "search", "Third line: internal audit", "independent assurance; reports\nto the audit committee", PURPLE, step=5, icon_size=44, title_size=15)
t.arrow([(450, 162), (330, 206)], None, INK, step=2, width=2.2); t.arrow([(250, 312), (190, 356)], None, INK, step=3, width=2.2); t.arrow([(390, 312), (530, 356)], None, INK, step=4, width=2.2)
t.arrow([(334, 440), (404, 440)], "challenges", ORANGE, step=4, size=11, both=True, width=2, label_dy=-10)
t.arrow([(910, 256), (680, 120)], None, PURPLE, step=5, width=2.4); t.text(812, 170, "reports directly", 12, PURPLE, "bold", "start", step=5)
t.arrow([(756, 330), (620, 356)], None, PURPLE, step=6, dash=True, width=1.8); t.arrow([(756, 345), (280, 356)], None, PURPLE, step=6, dash=True, width=1.6)
t.text(880, 440, "audits both lines", 13, PURPLE, "bold", step=6)
for n_, (x, y) in enumerate([(390, 60), (160, 220), (40, 370), (420, 370), (770, 270), (790, 420)], 1): t.badge(n_, x, y, step=n_)
t.save(OUT + "ch19_three_lines")

# Exception workflow
e = Fig(1100, 460, "An exception is a time-limited risk decision, not a permanent waiver",
        "A request names the requirement, scope, and business reason. A compensating control is proposed, the residual risk is rated, "
        "and the exception is approved at the level the rating requires. It carries an expiry date and a remediation plan. At expiry, "
        "a remediated exception is closed; one not remediated goes back to be re-rated.")
st = [("document", "Request", "requirement, scope,\nbusiness reason"), ("shield", "Compensating\ncontrol", "proposed"), ("warning", "Residual risk", "rated"),
      ("idcard", "Approved", "at the level the\nrating requires"), ("clock", "Expiry date", "and remediation plan")]
for i, (ic, name, sub) in enumerate(st):
    x = 90 + i * 195
    e.circle(x, 150, 52, "#ffffff", BLUE, 3, step=i + 1); e.icon(ic, x, 146, 58, step=i + 1)
    e.text(x, 230, name, 14, BLUE, "bold", step=i + 1); e.text(x, 268 if "\n" in name else 250, sub, 12, INK, step=i + 1); e.badge(i + 1, x - 42, 108, step=i + 1)
    if i < 4: e.arrow([(x + 54, 150), (x + 141, 150)], None, BLUE, step=i + 2, width=2.6)
e.poly([(1010, 100), (1060, 150), (1010, 200), (960, 150)], "#f4f6f8", "#52606d", 2, step=6); e.text(1010, 156, "Expired?", 13, INK, "bold", step=6)
e.arrow([(924, 150), (958, 150)], None, BLUE, step=6, width=2.4); e.badge(6, 1010, 88, step=6)
e.icon("check", 1010, 330, 40, "Closed", step=7, label_size=13); e.arrow([(1010, 202), (1010, 304)], "remediated", GREEN, step=7, size=12, label_anchor="end", label_dy=4, width=2.4)
e.arrow([(985, 186), (940, 310), (480, 310), (480, 280)], "not remediated: re-rate", RED, step=8, size=12, width=2.4, label_at=.55, dash=True)
e.badge(7, 1050, 310, step=7, color=GREEN); e.badge(8, 520, 310, step=8, color=RED)
e.text(550, 410, "No compensating control? Then it is a risk acceptance and should be routed as one.", 13, MUTED, italic=True, step=8)
e.save(OUT + "ch19_exception_flow")

# Decision rights
d = Fig(1100, 520, "Decision rights on one real decision: who is Responsible, Accountable, Consulted, Informed",
        "Three bodies: the board or its audit and risk committee oversees; the executive steering committee prioritizes, funds, and "
        "owns exceptions above the CISO's authority; technical bodies such as a change advisory board apply the standards. For an "
        "internet-facing system that cannot be patched before a release freeze, the system owner is accountable, the platform team is "
        "responsible for compensating controls, security and legal are consulted, and the steering committee is informed through the "
        "exception register.")
bodies = [("bank", "Board, audit and risk committee", "oversees"), ("group", "Executive steering committee", "prioritizes, funds, owns\nexceptions above the CISO"),
          ("gear", "Technical bodies, e.g. CAB", "apply the standards")]
for i, (ic, name, sub) in enumerate(bodies):
    y = 70 + i * 110
    d.rect(30, y, 380, 92, "#f4f6f8", "#5b6570", 1.6, rx=8, step=1); d.icon(ic, 74, y + 46, 46, step=1)
    d.text(110, y + 38, name, 14, INK, "bold", "start", step=1); d.text(110, y + 58, sub, 12, INK, anchor="start", step=1)
d.badge(1, 30, 70, step=1)
d.icon("server", 600, 120, 70, "Internet-facing system", "cannot be patched before a freeze", step=2); d.icon("warning", 634, 90, 24, step=2); d.badge(2, 550, 70, step=2, color=ORANGE)
raci = [("A", "Accountable", "system owner (one name)", "user2", RED), ("R", "Responsible", "platform team: compensating controls", "user-laptop", BLUE),
        ("C", "Consulted", "security (rates residual risk), legal", "shield", ORANGE), ("I", "Informed", "steering committee via the exception register", "logbook", GREEN)]
for i, (k, name, who, ic, col) in enumerate(raci):
    y = 230 + i * 66
    d.circle(470, y + 22, 20, col, col, 1, step=3 + i); d.text(470, y + 29, k, 18, "#ffffff", "bold", step=3 + i)
    d.icon(ic, 520, y + 22, 36, step=3 + i); d.text(550, y + 16, name, 15, col, "bold", "start", step=3 + i); d.text(550, y + 36, who, 13, INK, anchor="start", step=3 + i)
    d.badge(3 + i, 440, y, step=3 + i, color=col)
d.rect(30, 400, 380, 100, "#fff8e1", "#d9a400", 1.6, rx=8, step=7); d.icon("clock", 70, 450, 36, step=7); d.badge(7, 30, 400, step=7, color=ORANGE)
d.text(100, 436, "The test: ask three people to name", 13, INK, "bold", "start", step=7); d.text(100, 456, "the accountable person. More than a", 13, INK, "bold", "start", step=7)
d.text(100, 476, "minute, or more than one name: decorative.", 13, INK, "bold", "start", step=7)
d.save(OUT + "ch19_decision_rights")
print("ok")
