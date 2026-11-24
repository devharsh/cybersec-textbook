"""Original device and actor icons for book figures, drawn in a 100 x 100 box.
Glossy network-diagram style: soft gradients, darker outlines, a ground shadow."""

GRADS = """
<linearGradient id="g-steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a5361"/><stop offset=".5" stop-color="#2b313a"/><stop offset="1" stop-color="#1c2027"/></linearGradient>
<linearGradient id="g-steel-top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8796"/><stop offset="1" stop-color="#4a5361"/></linearGradient>
<linearGradient id="g-silver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f8"/><stop offset="1" stop-color="#b9c0c9"/></linearGradient>
<linearGradient id="g-silver-side" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8dde3"/><stop offset="1" stop-color="#9aa3ae"/></linearGradient>
<linearGradient id="g-screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5fc3ff"/><stop offset=".55" stop-color="#1e88e5"/><stop offset="1" stop-color="#0b4f9c"/></linearGradient>
<linearGradient id="g-router" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb6e8"/><stop offset="1" stop-color="#1f5f99"/></linearGradient>
<linearGradient id="g-router-top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9f4fc"/><stop offset="1" stop-color="#a9cdea"/></linearGradient>
<linearGradient id="g-db" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8e99a6"/><stop offset=".45" stop-color="#e3e7eb"/><stop offset="1" stop-color="#7b8693"/></linearGradient>
<linearGradient id="g-brick" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2774f"/><stop offset="1" stop-color="#b2472a"/></linearGradient>
<linearGradient id="g-cloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#b8dcf5"/></linearGradient>
<linearGradient id="g-skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7d7bf"/><stop offset="1" stop-color="#e2b394"/></linearGradient>
<linearGradient id="g-suit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4b5563"/><stop offset="1" stop-color="#1f2733"/></linearGradient>
<linearGradient id="g-suit2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7b5ea7"/><stop offset="1" stop-color="#46336b"/></linearGradient>
<linearGradient id="g-hood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f47"/><stop offset="1" stop-color="#0f1216"/></linearGradient>
<linearGradient id="g-robot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8eef5"/><stop offset="1" stop-color="#9fb0c3"/></linearGradient>
<linearGradient id="g-gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="#d49a1f"/></linearGradient>
<linearGradient id="g-paper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e4e9ef"/></linearGradient>
<linearGradient id="g-green" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fd38b"/><stop offset="1" stop-color="#2e8b45"/></linearGradient>
<linearGradient id="g-red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a80"/><stop offset="1" stop-color="#c62828"/></linearGradient>
<radialGradient id="g-shadow"><stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
"""

SHADOW = '<ellipse cx="50" cy="95" rx="38" ry="4.5" fill="url(#g-shadow)"/>'

ICONS = {}

ICONS["server"] = SHADOW + """
<path d="M28 16 L40 8 L72 8 L60 16 Z" fill="url(#g-steel-top)" stroke="#14181d" stroke-width="1"/>
<path d="M60 16 L72 8 L72 82 L60 91 Z" fill="#1b1f25" stroke="#14181d" stroke-width="1"/>
<rect x="28" y="16" width="32" height="75" rx="1.5" fill="url(#g-steel)" stroke="#14181d" stroke-width="1"/>
<g fill="#59626f" stroke="#14181d" stroke-width=".6">
<rect x="32" y="21" width="24" height="5" rx="1"/><rect x="32" y="28" width="24" height="5" rx="1"/>
<rect x="32" y="35" width="24" height="5" rx="1"/><rect x="32" y="42" width="24" height="5" rx="1"/></g>
<g fill="#8fd16a"><circle cx="53" cy="23.5" r="1"/><circle cx="53" cy="30.5" r="1"/><circle cx="53" cy="37.5" r="1"/></g>
<g stroke="#3d4450" stroke-width="1"><line x1="32" y1="56" x2="56" y2="56"/><line x1="32" y1="60" x2="56" y2="60"/><line x1="32" y1="64" x2="56" y2="64"/></g>
<circle cx="44" cy="80" r="3" fill="#2196f3" stroke="#0d47a1" stroke-width=".8"/>
"""

ICONS["rack"] = SHADOW + """
<rect x="24" y="10" width="52" height="82" rx="3" fill="url(#g-steel)" stroke="#14181d" stroke-width="1.2"/>
""" + "".join(f'<rect x="29" y="{15+i*15}" width="42" height="11" rx="1.5" fill="#3b424d" stroke="#14181d" stroke-width=".7"/>'
              f'<rect x="32" y="{18+i*15}" width="20" height="5" rx="1" fill="#55606e"/>'
              f'<circle cx="64" cy="{20.5+i*15}" r="1.4" fill="#8fd16a"/><circle cx="68" cy="{20.5+i*15}" r="1.4" fill="#4fc3f7"/>' for i in range(5))

ICONS["database"] = SHADOW + """
<path d="M24 22 v56 a26 9 0 0 0 52 0 v-56" fill="url(#g-db)" stroke="#4f5964" stroke-width="1.2"/>
<path d="M24 41 a26 9 0 0 0 52 0 M24 60 a26 9 0 0 0 52 0" fill="none" stroke="#5f6a76" stroke-width="1.2"/>
<ellipse cx="50" cy="22" rx="26" ry="9" fill="#f1f3f5" stroke="#4f5964" stroke-width="1.2"/>
<ellipse cx="50" cy="22" rx="18" ry="5" fill="#dfe4e9"/>
"""

ICONS["desktop"] = SHADOW + """
<rect x="12" y="14" width="58" height="44" rx="3" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.2"/>
<rect x="16" y="18" width="50" height="35" rx="1" fill="url(#g-screen)"/>
<path d="M16 18 h50 v14 Q40 26 16 34 Z" fill="#fff" opacity=".18"/>
<path d="M36 58 h10 l3 14 h-16 Z" fill="url(#g-silver-side)" stroke="#5b6570" stroke-width="1"/>
<rect x="26" y="72" width="30" height="4" rx="2" fill="#9aa3ae" stroke="#5b6570" stroke-width=".8"/>
<rect x="72" y="30" width="18" height="60" rx="2" fill="url(#g-steel)" stroke="#14181d" stroke-width="1"/>
<rect x="75" y="35" width="12" height="3" rx="1" fill="#5c6672"/><rect x="75" y="41" width="12" height="3" rx="1" fill="#5c6672"/>
<circle cx="81" cy="80" r="2" fill="#4fc3f7"/>
<path d="M20 82 h44 l4 8 h-52 Z" fill="#cfd5dc" stroke="#5b6570" stroke-width=".8"/>
"""

ICONS["laptop"] = SHADOW + """
<rect x="20" y="22" width="60" height="42" rx="3" fill="#2f353d" stroke="#14181d" stroke-width="1.2"/>
<rect x="24" y="26" width="52" height="34" rx="1" fill="url(#g-screen)"/>
<path d="M24 26 h52 v12 Q50 31 24 41 Z" fill="#fff" opacity=".18"/>
<path d="M12 70 L20 64 H80 L88 70 Z" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1"/>
<rect x="12" y="70" width="76" height="5" rx="2" fill="#9aa3ae" stroke="#5b6570" stroke-width=".8"/>
<rect x="42" y="66" width="16" height="2.4" rx="1" fill="#8892a0"/>
"""

ICONS["phone"] = SHADOW + """
<rect x="32" y="10" width="36" height="80" rx="7" fill="#22272e" stroke="#0d1014" stroke-width="1.2"/>
<rect x="35.5" y="18" width="29" height="62" rx="2" fill="url(#g-screen)"/>
<path d="M35.5 18 h29 v18 Q50 30 35.5 40 Z" fill="#fff" opacity=".18"/>
<rect x="44" y="13" width="12" height="2" rx="1" fill="#555d68"/>
<circle cx="50" cy="85" r="2.2" fill="#3a414b"/>
"""

ICONS["router"] = SHADOW + """
<path d="M14 44 v22 a36 12 0 0 0 72 0 v-22" fill="url(#g-router)" stroke="#164b78" stroke-width="1.2"/>
<ellipse cx="50" cy="44" rx="36" ry="12" fill="url(#g-router-top)" stroke="#164b78" stroke-width="1.2"/>
<g fill="#1565c0" stroke="#0d3c6e" stroke-width=".5">
<path d="M50 34 l-5 4 h3 v4 h4 v-4 h3 Z"/><path d="M50 54 l-5 -4 h3 v-4 h4 v4 h3 Z" transform="translate(0,0)"/>
<path d="M28 44 l4 -3.5 v2.3 h6 v2.4 h-6 v2.3 Z"/><path d="M72 44 l-4 -3.5 v2.3 h-6 v2.4 h6 v2.3 Z"/></g>
<g fill="#cfe6f7"><circle cx="30" cy="70" r="1.5"/><circle cx="36" cy="72" r="1.5"/><circle cx="42" cy="73" r="1.5"/></g>
"""

ICONS["switch"] = SHADOW + """
<path d="M10 46 L24 36 H90 L76 46 Z" fill="url(#g-router-top)" stroke="#164b78" stroke-width="1.2"/>
<path d="M10 46 H76 V66 H10 Z" fill="url(#g-router)" stroke="#164b78" stroke-width="1.2"/>
<path d="M76 46 L90 36 V56 L76 66 Z" fill="#174f80" stroke="#164b78" stroke-width="1.2"/>
""" + "".join(f'<rect x="{15+i*7.2}" y="52" width="5" height="4" rx=".6" fill="#0d2f50"/><rect x="{15+i*7.2}" y="58" width="5" height="4" rx=".6" fill="#0d2f50"/>' for i in range(8)) + """
<g fill="#1565c0"><path d="M38 41 h12 v-2.4 l5 3.4 -5 3.4 v-2.4 h-12 Z"/><path d="M62 41 h-12" stroke="#1565c0"/></g>
"""

ICONS["firewall"] = SHADOW + """
<rect x="14" y="26" width="72" height="62" rx="2" fill="url(#g-brick)" stroke="#7a2e18" stroke-width="1.2"/>
<g stroke="#f6d3c4" stroke-width="2.2" fill="none">
<path d="M14 41 H86 M14 57 H86 M14 73 H86"/>
<path d="M38 26 V41 M62 26 V41 M26 41 V57 M50 41 V57 M74 41 V57 M38 57 V73 M62 57 V73 M26 73 V88 M50 73 V88 M74 73 V88"/></g>
<path d="M50 4 C58 14 66 16 62 26 H38 C34 18 44 14 50 4 Z" fill="#ffb300" stroke="#e65100" stroke-width="1"/>
<path d="M50 12 C55 18 57 21 55 26 H45 C43 21 47 18 50 12 Z" fill="#fff176"/>
"""

ICONS["cloud"] = """
<path d="M22 74 C8 74 4 56 18 50 C16 34 36 26 46 36 C52 20 78 22 80 42 C96 42 98 72 80 74 Z"
 fill="url(#g-cloud)" stroke="#5b9bd5" stroke-width="2"/>
<path d="M26 66 C20 66 18 60 22 58" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/>
"""

def _person(suit, hair, female=False, prop=None):
    hairpath = ('<path d="M33 30 C33 12 67 12 67 30 L68 46 C64 40 62 34 60 30 C52 32 44 31 38 26 C36 34 34 40 32 46 Z" fill="%s"/>' % hair
                if female else
                '<path d="M35 28 C34 14 66 12 66 28 C62 22 52 20 44 22 C40 23 37 25 35 28 Z" fill="%s"/>' % hair)
    body = f'''{SHADOW}
<path d="M18 94 C18 66 32 58 50 58 C68 58 82 66 82 94 Z" fill="url(#{suit})" stroke="#11161c" stroke-width="1"/>
<path d="M44 58 L50 70 L56 58 Z" fill="#fff"/>{'' if female else '<path d="M48.5 60 L51.5 60 L52.5 76 L50 80 L47.5 76 Z" fill="#c62828"/>'}
<rect x="45" y="48" width="10" height="11" fill="url(#g-skin)"/>
<ellipse cx="50" cy="34" rx="15" ry="17" fill="url(#g-skin)" stroke="#c89273" stroke-width=".8"/>
{hairpath}'''
    if prop == "phone":
        body += '<rect x="66" y="64" width="13" height="22" rx="2.5" fill="#22272e" transform="rotate(18 72 75)"/><rect x="68" y="67" width="9" height="15" rx="1" fill="url(#g-screen)" transform="rotate(18 72 75)"/>'
    if prop == "laptop":
        body += '<path d="M58 78 L88 70 L92 88 L62 94 Z" fill="#2f353d"/><path d="M60.5 79.5 L86 73 L89 86 L63 92 Z" fill="url(#g-screen)"/>'
    return body

ICONS["user"] = _person("g-suit", "#3b2a20")
ICONS["user-laptop"] = _person("g-suit", "#3b2a20", prop="laptop")
ICONS["user2"] = _person("g-suit2", "#1f1a17", female=True)
ICONS["user2-phone"] = _person("g-suit2", "#1f1a17", female=True, prop="phone")

ICONS["attacker"] = SHADOW + """
<path d="M16 94 C16 64 30 54 50 54 C70 54 84 64 84 94 Z" fill="url(#g-hood)" stroke="#000" stroke-width="1"/>
<path d="M28 52 C26 22 40 10 50 10 C60 10 74 22 72 52 C66 60 34 60 28 52 Z" fill="url(#g-hood)" stroke="#000" stroke-width="1"/>
<ellipse cx="50" cy="40" rx="15" ry="16" fill="#0a0c0f"/>
<path d="M40 38 l7 2.5 -7 2 Z M60 38 l-7 2.5 7 2 Z" fill="#ff3b30"/>
<path d="M30 74 L70 74 L74 92 L26 92 Z" fill="#3a414b" stroke="#000" stroke-width=".8"/>
<rect x="33" y="77" width="34" height="12" fill="#b71c1c" opacity=".85"/>
<path d="M46 80 a4 4 0 0 1 8 0 v1 h-8 Z M45 81 h10 v6 h-10 Z" fill="#ffcdd2"/>
"""

ICONS["robot"] = SHADOW + """
<line x1="50" y1="8" x2="50" y2="18" stroke="#5b6b7d" stroke-width="2.5"/><circle cx="50" cy="7" r="4" fill="#ff9800" stroke="#e65100"/>
<rect x="24" y="18" width="52" height="40" rx="11" fill="url(#g-robot)" stroke="#4d5d70" stroke-width="1.4"/>
<rect x="31" y="27" width="38" height="20" rx="7" fill="#183247"/>
<circle cx="42" cy="37" r="4" fill="#4dd0e1"/><circle cx="58" cy="37" r="4" fill="#4dd0e1"/>
<rect x="18" y="32" width="6" height="12" rx="2" fill="#7d8ea2"/><rect x="76" y="32" width="6" height="12" rx="2" fill="#7d8ea2"/>
<path d="M30 92 V70 a8 8 0 0 1 8 -8 h24 a8 8 0 0 1 8 8 V92 Z" fill="url(#g-robot)" stroke="#4d5d70" stroke-width="1.4"/>
<rect x="40" y="70" width="20" height="10" rx="2" fill="#183247"/><circle cx="45" cy="75" r="1.8" fill="#8fd16a"/><circle cx="55" cy="75" r="1.8" fill="#ff7043"/>
"""

ICONS["bank"] = SHADOW + """
<path d="M12 34 L50 12 L88 34 Z" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.2"/>
<rect x="14" y="34" width="72" height="6" fill="#cfd5dc" stroke="#5b6570" stroke-width="1"/>
""" + "".join(f'<rect x="{20+i*16}" y="42" width="9" height="38" fill="url(#g-silver-side)" stroke="#5b6570" stroke-width=".8"/>' for i in range(5)) + """
<rect x="10" y="80" width="80" height="8" fill="#b9c0c9" stroke="#5b6570" stroke-width="1"/>
<circle cx="50" cy="25" r="4.5" fill="url(#g-gold)" stroke="#a5760e"/>
"""

ICONS["document"] = SHADOW + """
<path d="M26 8 H62 L76 22 V90 H26 Z" fill="url(#g-paper)" stroke="#6b7785" stroke-width="1.2"/>
<path d="M62 8 V22 H76" fill="#d5dbe2" stroke="#6b7785" stroke-width="1.2"/>
<g stroke="#9aa6b3" stroke-width="2.4" stroke-linecap="round"><line x1="34" y1="34" x2="68" y2="34"/><line x1="34" y1="44" x2="68" y2="44"/><line x1="34" y1="54" x2="60" y2="54"/><line x1="34" y1="64" x2="66" y2="64"/></g>
"""

ICONS["certificate"] = SHADOW + """
<rect x="12" y="16" width="76" height="56" rx="3" fill="url(#g-paper)" stroke="#6b7785" stroke-width="1.2"/>
<rect x="17" y="21" width="66" height="46" rx="2" fill="none" stroke="#c9a227" stroke-width="1.4"/>
<g stroke="#9aa6b3" stroke-width="2.2" stroke-linecap="round"><line x1="24" y1="32" x2="62" y2="32"/><line x1="24" y1="41" x2="56" y2="41"/><line x1="24" y1="50" x2="50" y2="50"/></g>
<path d="M66 60 l-5 26 7 -5 7 5 -5 -26" fill="#c62828"/>
<circle cx="70" cy="56" r="10" fill="url(#g-gold)" stroke="#a5760e" stroke-width="1.2"/>
"""

ICONS["key"] = """
<circle cx="32" cy="50" r="18" fill="url(#g-gold)" stroke="#a5760e" stroke-width="2"/>
<circle cx="28" cy="50" r="6" fill="#fff8e1" stroke="#a5760e" stroke-width="1.5"/>
<path d="M48 45 H90 V55 H84 V64 H76 V55 H70 V62 H62 V55 H48 Z" fill="url(#g-gold)" stroke="#a5760e" stroke-width="2"/>
"""

ICONS["lock"] = SHADOW + """
<path d="M32 44 V30 a18 18 0 0 1 36 0 V44" fill="none" stroke="#7d8796" stroke-width="7"/>
<rect x="22" y="42" width="56" height="44" rx="6" fill="url(#g-gold)" stroke="#a5760e" stroke-width="1.4"/>
<circle cx="50" cy="60" r="6" fill="#5d4006"/><rect x="47.5" y="62" width="5" height="12" rx="2" fill="#5d4006"/>
"""

ICONS["envelope"] = SHADOW + """
<rect x="12" y="26" width="76" height="52" rx="3" fill="url(#g-paper)" stroke="#6b7785" stroke-width="1.4"/>
<path d="M12 28 L50 56 L88 28" fill="none" stroke="#6b7785" stroke-width="1.6"/>
"""

ICONS["shield"] = SHADOW + """
<path d="M50 8 L84 20 V48 C84 70 68 84 50 92 C32 84 16 70 16 48 V20 Z" fill="url(#g-green)" stroke="#1b5e20" stroke-width="1.6"/>
<path d="M36 50 L46 60 L66 38" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
"""

ICONS["devil"] = """
<path d="M24 30 L18 8 L38 22 Z M76 30 L82 8 L62 22 Z" fill="#b71c1c"/>
<circle cx="50" cy="52" r="32" fill="url(#g-red)" stroke="#7f0000" stroke-width="1.6"/>
<path d="M34 44 l10 4 M66 44 l-10 4" stroke="#3e0000" stroke-width="4" stroke-linecap="round"/>
<circle cx="40" cy="52" r="4" fill="#fff"/><circle cx="60" cy="52" r="4" fill="#fff"/>
<circle cx="41" cy="53" r="2" fill="#000"/><circle cx="59" cy="53" r="2" fill="#000"/>
<path d="M36 66 Q50 78 64 66" fill="none" stroke="#3e0000" stroke-width="3.5" stroke-linecap="round"/>
"""

ICONS["bot"] = SHADOW + """
<rect x="20" y="30" width="60" height="44" rx="3" fill="#2f353d" stroke="#14181d" stroke-width="1.2"/>
<rect x="24" y="34" width="52" height="34" rx="1" fill="#4a0000"/>
<circle cx="50" cy="48" r="9" fill="#e53935"/><path d="M44 58 h12 v4 h-12 Z" fill="#e53935"/>
<path d="M12 80 L20 74 H80 L88 80 Z" fill="#7b8693" stroke="#3d4450" stroke-width="1"/>
"""

ICONS["gear"] = """
<path d="M50 10 l7 2 2 10 8 4 9 -5 5 5 -5 9 4 8 10 2 2 7 -2 7 -10 2 -4 8 5 9 -5 5 -9 -5 -8 4 -2 10 -7 2 -7 -2 -2 -10 -8 -4 -9 5 -5 -5 5 -9 -4 -8 -10 -2 -2 -7 2 -7 10 -2 4 -8 -5 -9 5 -5 9 5 8 -4 2 -10 Z"
 fill="url(#g-steel-top)" stroke="#3d4450" stroke-width="1.4"/>
<circle cx="50" cy="50" r="14" fill="#eef1f4" stroke="#3d4450" stroke-width="1.4"/>
"""

ICONS["plc"] = SHADOW + """
<rect x="14" y="20" width="72" height="66" rx="3" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.2"/>
<rect x="20" y="26" width="26" height="18" rx="1" fill="#0b4f9c"/><text x="33" y="39" font-size="10" text-anchor="middle" fill="#bfe3ff" font-family="Helvetica,Arial,sans-serif">PLC</text>
""" + "".join(f'<rect x="{52+i*8}" y="26" width="5" height="18" rx="1" fill="#3b424d"/><circle cx="{54.5+i*8}" cy="{30}" r="1.3" fill="#8fd16a"/>' for i in range(4)) + """
""" + "".join(f'<rect x="{20+i*8.5}" y="56" width="6" height="22" rx="1" fill="#2f353d"/>' for i in range(8))

def defs(used):
    out = ["<defs>", globals()["GRADS"]]
    for name in used:
        out.append(f'<symbol id="i-{name}" viewBox="0 0 100 100">{ICONS[name]}</symbol>')
    out.append("</defs>")
    return "\n".join(out)

ICONS["idcard"] = SHADOW + """
<rect x="10" y="22" width="80" height="54" rx="5" fill="url(#g-paper)" stroke="#4a6fa5" stroke-width="1.6"/>
<rect x="10" y="22" width="80" height="12" rx="5" fill="#4a6fa5"/><rect x="10" y="29" width="80" height="5" fill="#4a6fa5"/>
<rect x="17" y="40" width="24" height="28" rx="2" fill="#dbe7f5"/>
<circle cx="29" cy="50" r="6" fill="url(#g-skin)"/><path d="M19 68 C19 58 39 58 39 68 Z" fill="#4b5563"/>
<g stroke="#9aa6b3" stroke-width="3" stroke-linecap="round"><line x1="48" y1="46" x2="82" y2="46"/><line x1="48" y1="55" x2="76" y2="55"/><line x1="48" y1="64" x2="70" y2="64"/></g>
"""
ICONS["checklist"] = SHADOW + """
<rect x="22" y="14" width="56" height="76" rx="4" fill="url(#g-paper)" stroke="#6b7785" stroke-width="1.4"/>
<rect x="38" y="9" width="24" height="10" rx="3" fill="#7d8796"/>
""" + "".join(f'<path d="M30 {32+i*16} l4 4 8 -9" fill="none" stroke="#2e7d32" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<line x1="48" y1="{33+i*16}" x2="70" y2="{33+i*16}" stroke="#9aa6b3" stroke-width="3" stroke-linecap="round"/>' for i in range(3)) + """
<line x1="30" y1="81" x2="70" y2="81" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>
"""
ICONS["logbook"] = SHADOW + """
<rect x="22" y="12" width="58" height="78" rx="3" fill="#8d6e63" stroke="#4e342e" stroke-width="1.4"/>
<rect x="28" y="16" width="50" height="70" rx="2" fill="url(#g-paper)"/>
""" + "".join(f'<line x1="34" y1="{26+i*9}" x2="72" y2="{26+i*9}" stroke="#9aa6b3" stroke-width="2.2"/>' for i in range(7)) + """
<g fill="#6b7785" font-family="Courier, monospace" font-size="6"><text x="34" y="24">09:14</text><text x="34" y="33">09:15</text></g>
"""
ICONS["eye"] = """
<path d="M8 50 C26 22 74 22 92 50 C74 78 26 78 8 50 Z" fill="url(#g-paper)" stroke="#2f6fae" stroke-width="3"/>
<circle cx="50" cy="50" r="17" fill="url(#g-screen)" stroke="#0b4f9c" stroke-width="2"/>
<circle cx="50" cy="50" r="7" fill="#0d1b2a"/><circle cx="44" cy="44" r="3.5" fill="#fff"/>
"""
ICONS["clock"] = SHADOW + """
<circle cx="50" cy="50" r="38" fill="url(#g-paper)" stroke="#2f6fae" stroke-width="5"/>
""" + "".join(f'<line x1="50" y1="17" x2="50" y2="23" stroke="#52606d" stroke-width="3" transform="rotate({a} 50 50)"/>' for a in range(0,360,30)) + """
<line x1="50" y1="50" x2="50" y2="27" stroke="#1f2933" stroke-width="4" stroke-linecap="round"/>
<line x1="50" y1="50" x2="68" y2="58" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>
<circle cx="50" cy="50" r="3.5" fill="#1f2933"/>
"""
ICONS["hourglass"] = SHADOW + """
<rect x="24" y="8" width="52" height="8" rx="3" fill="#8d6e63" stroke="#4e342e"/><rect x="24" y="84" width="52" height="8" rx="3" fill="#8d6e63" stroke="#4e342e"/>
<path d="M30 16 H70 C70 36 54 42 54 50 C54 58 70 64 70 84 H30 C30 64 46 58 46 50 C46 42 30 36 30 16 Z" fill="#e3f2fd" stroke="#5b9bd5" stroke-width="2"/>
<path d="M36 26 H64 C62 36 52 42 50 47 C48 42 38 36 36 26 Z" fill="#f2b84b"/>
<path d="M34 82 H66 C64 72 56 68 50 66 C44 68 36 72 34 82 Z" fill="#f2b84b"/>
"""
ICONS["nodes"] = """
<g stroke="#5b9bd5" stroke-width="3"><line x1="50" y1="20" x2="20" y2="70"/><line x1="50" y1="20" x2="80" y2="70"/><line x1="20" y1="70" x2="80" y2="70"/><line x1="50" y1="20" x2="50" y2="52"/><line x1="20" y1="70" x2="50" y2="52"/><line x1="80" y1="70" x2="50" y2="52"/></g>
""" + "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="url(#g-router)" stroke="#164b78" stroke-width="1.6"/>' for x, y in [(50,20),(20,70),(80,70),(50,52)])
ICONS["group"] = SHADOW + """
<g transform="translate(-18,4) scale(.8)">""" + ICONS["user2"].replace(SHADOW,"") + """</g>
<g transform="translate(38,4) scale(.8)">""" + ICONS["user"].replace(SHADOW,"") + """</g>
<g transform="translate(10,14) scale(.86)">""" + ICONS["user"].replace(SHADOW,"").replace("g-suit)", "g-suit3)") + """</g>
"""
GRADS = GRADS + '<linearGradient id="g-suit3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e86c1"/><stop offset="1" stop-color="#1b4f72"/></linearGradient>'
ICONS["chip"] = SHADOW + """
<rect x="24" y="24" width="52" height="52" rx="4" fill="#2f353d" stroke="#14181d" stroke-width="1.4"/>
<rect x="34" y="34" width="32" height="32" rx="2" fill="#4a5361"/><text x="50" y="55" font-size="12" text-anchor="middle" fill="#cfd8e3" font-family="Helvetica,Arial,sans-serif" font-weight="bold">CPU</text>
""" + "".join(f'<rect x="{30+i*9}" y="14" width="4" height="10" fill="#c9a227"/><rect x="{30+i*9}" y="76" width="4" height="10" fill="#c9a227"/>'
              f'<rect x="14" y="{30+i*9}" width="10" height="4" fill="#c9a227"/><rect x="76" y="{30+i*9}" width="10" height="4" fill="#c9a227"/>' for i in range(5))
ICONS["memory"] = SHADOW + """
<rect x="8" y="34" width="84" height="30" rx="2" fill="#2e7d32" stroke="#1b5e20" stroke-width="1.4"/>
""" + "".join(f'<rect x="{13+i*20}" y="38" width="14" height="18" rx="1" fill="#1f2933"/>' for i in range(4)) + "".join(
    f'<rect x="{12+i*5}" y="64" width="3" height="7" fill="#c9a227"/>' for i in range(16))
ICONS["bug"] = """
<ellipse cx="50" cy="56" rx="20" ry="26" fill="url(#g-red)" stroke="#7f0000" stroke-width="1.6"/>
<circle cx="50" cy="28" r="11" fill="#3e0000"/><line x1="50" y1="32" x2="50" y2="82" stroke="#7f0000" stroke-width="2"/>
<g stroke="#3e0000" stroke-width="3" stroke-linecap="round"><path d="M31 46 l-14 -8 M31 58 h-16 M32 70 l-14 8 M69 46 l14 -8 M69 58 h16 M68 70 l14 8 M44 20 l-6 -10 M56 20 l6 -10"/></g>
<circle cx="43" cy="50" r="4" fill="#3e0000"/><circle cx="57" cy="64" r="4" fill="#3e0000"/>
"""
ICONS["factory"] = SHADOW + """
<path d="M10 90 V48 L30 36 V48 L50 36 V48 L70 36 V22 H82 V90 Z" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.4"/>
""" + "".join(f'<rect x="{18+i*16}" y="60" width="9" height="12" fill="#5fc3ff" stroke="#0b4f9c"/>' for i in range(4)) + """
<rect x="70" y="10" width="12" height="12" fill="#c0392b"/><path d="M76 8 c-6 -6 4 -8 8 -4" fill="none" stroke="#9aa5b1" stroke-width="3"/>
"""
ICONS["hmi"] = SHADOW + """
<rect x="12" y="18" width="76" height="56" rx="4" fill="#3b424d" stroke="#14181d" stroke-width="1.4"/>
<rect x="18" y="24" width="64" height="44" rx="2" fill="#e8f5e9"/>
<path d="M24 56 L36 44 L46 50 L58 34 L74 42" fill="none" stroke="#2e7d32" stroke-width="2.4"/>
<rect x="24" y="28" width="16" height="8" rx="1" fill="#c0392b"/><rect x="44" y="28" width="16" height="8" rx="1" fill="#2e86c1"/>
<rect x="40" y="74" width="20" height="10" fill="#5b6570"/><rect x="28" y="84" width="44" height="5" rx="2" fill="#7d8796"/>
"""
ICONS["code"] = SHADOW + """
<rect x="10" y="16" width="80" height="66" rx="4" fill="#1e2530" stroke="#0d1014" stroke-width="1.4"/>
<rect x="10" y="16" width="80" height="11" rx="4" fill="#3b424d"/><circle cx="18" cy="21.5" r="2.2" fill="#ff5f56"/><circle cx="25" cy="21.5" r="2.2" fill="#ffbd2e"/><circle cx="32" cy="21.5" r="2.2" fill="#27c93f"/>
<path d="M30 42 L20 52 L30 62 M70 42 L80 52 L70 62" fill="none" stroke="#4fc3f7" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="56" y1="38" x2="44" y2="66" stroke="#8fd16a" stroke-width="4" stroke-linecap="round"/>
"""
ICONS["search"] = """
<circle cx="42" cy="42" r="24" fill="#e3f2fd" stroke="#2f6fae" stroke-width="7"/>
<line x1="60" y1="60" x2="86" y2="86" stroke="#5b6570" stroke-width="11" stroke-linecap="round"/>
<path d="M30 34 a14 14 0 0 1 12 -8" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
"""
ICONS["warning"] = """
<path d="M50 10 L92 86 H8 Z" fill="url(#g-gold)" stroke="#a5760e" stroke-width="3" stroke-linejoin="round"/>
<rect x="46" y="36" width="8" height="28" rx="3" fill="#3e2a00"/><circle cx="50" cy="73" r="5" fill="#3e2a00"/>
"""
ICONS["check"] = """<circle cx="50" cy="50" r="38" fill="url(#g-green)" stroke="#1b5e20" stroke-width="2"/>
<path d="M32 51 L45 64 L69 38" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>"""
ICONS["cross"] = """<circle cx="50" cy="50" r="38" fill="url(#g-red)" stroke="#7f0000" stroke-width="2"/>
<path d="M35 35 L65 65 M65 35 L35 65" stroke="#fff" stroke-width="9" stroke-linecap="round"/>"""

# ---- batch 3: access and wireless gear
ICONS["wifi"] = SHADOW + """
<path d="M26 26 L22 52" stroke="#3b424d" stroke-width="3.4" stroke-linecap="round"/><path d="M74 26 L78 52" stroke="#3b424d" stroke-width="3.4" stroke-linecap="round"/>
<path d="M14 58 L22 50 H82 L90 58 Z" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.2"/>
<path d="M14 58 H90 V76 H14 Z" fill="url(#g-steel-top)" stroke="#5b6570" stroke-width="1.2"/>
""" + "".join(f'<circle cx="{30+i*10}" cy="67" r="2" fill="{c}"/>' for i, c in enumerate(["#8fd16a", "#8fd16a", "#4fc3f7", "#4fc3f7", "#f5b041"])) + """
<g fill="none" stroke="#1e88e5" stroke-width="3" stroke-linecap="round">
<path d="M40 30 a14 14 0 0 1 20 0"/><path d="M34 23 a22 22 0 0 1 32 0"/><path d="M28 16 a30 30 0 0 1 44 0"/></g>
<circle cx="50" cy="36" r="3" fill="#1e88e5"/>
"""
ICONS["hub"] = SHADOW + """
<path d="M10 46 L24 36 H90 L76 46 Z" fill="#d7dce2" stroke="#5b6570" stroke-width="1.2"/>
<path d="M10 46 H76 V66 H10 Z" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.2"/>
<path d="M76 46 L90 36 V56 L76 66 Z" fill="#9aa3ae" stroke="#5b6570" stroke-width="1.2"/>
""" + "".join(f'<rect x="{15+i*12}" y="51" width="8" height="8" rx="1" fill="#3b424d"/><circle cx="{19+i*12}" cy="62.5" r="1.2" fill="#f5b041"/>' for i in range(5))
ICONS["satellite"] = SHADOW + """
<g transform="rotate(-30 50 48)">
<rect x="6" y="40" width="28" height="16" fill="#1f4e9c" stroke="#0d2c5c" stroke-width="1.2"/>
<rect x="66" y="40" width="28" height="16" fill="#1f4e9c" stroke="#0d2c5c" stroke-width="1.2"/>
<g stroke="#7fa6dd" stroke-width=".8"><line x1="13" y1="40" x2="13" y2="56"/><line x1="20" y1="40" x2="20" y2="56"/><line x1="27" y1="40" x2="27" y2="56"/>
<line x1="73" y1="40" x2="73" y2="56"/><line x1="80" y1="40" x2="80" y2="56"/><line x1="87" y1="40" x2="87" y2="56"/><line x1="6" y1="48" x2="34" y2="48"/><line x1="66" y1="48" x2="94" y2="48"/></g>
<line x1="34" y1="48" x2="40" y2="48" stroke="#5b6570" stroke-width="3"/><line x1="60" y1="48" x2="66" y2="48" stroke="#5b6570" stroke-width="3"/>
<rect x="40" y="36" width="20" height="24" rx="2" fill="url(#g-gold)" stroke="#8a6d1a" stroke-width="1.2"/>
<path d="M44 60 q6 10 12 0" fill="#d7dce2" stroke="#5b6570" stroke-width="1"/></g>
"""
ICONS["tower"] = SHADOW + """
<g stroke="#5b6570" stroke-width="2.6" fill="none" stroke-linecap="round">
<path d="M50 26 L34 92 M50 26 L66 92"/><path d="M40 66 L60 66 M37 80 L63 80 M43 50 L57 50"/><path d="M40 66 L57 50 M60 66 L43 50 M37 80 L60 66 M63 80 L40 66"/></g>
<circle cx="50" cy="24" r="4" fill="#c0392b"/>
<g fill="none" stroke="#1e88e5" stroke-width="2.8" stroke-linecap="round">
<path d="M38 14 a16 16 0 0 0 0 20"/><path d="M62 14 a16 16 0 0 1 0 20"/><path d="M30 8 a26 26 0 0 0 0 32"/><path d="M70 8 a26 26 0 0 1 0 32"/></g>
"""
ICONS["modem"] = SHADOW + """
<rect x="30" y="16" width="40" height="72" rx="6" fill="url(#g-steel-top)" stroke="#2b3138" stroke-width="1.4"/>
<rect x="34" y="20" width="32" height="6" rx="2" fill="#3b424d"/>
""" + "".join(f'<circle cx="50" cy="{36+i*9}" r="2.4" fill="{c}"/>' for i, c in enumerate(["#8fd16a", "#8fd16a", "#4fc3f7", "#4fc3f7", "#f5b041"])) + """
<rect x="24" y="84" width="52" height="6" rx="2" fill="#9aa3ae"/>
"""
ICONS["door"] = SHADOW + """
<rect x="24" y="10" width="52" height="82" fill="#9aa3ae" stroke="#5b6570" stroke-width="1.4"/>
<rect x="29" y="14" width="42" height="78" fill="url(#g-brick)" stroke="#6d3b1e" stroke-width="1.2"/>
<rect x="34" y="20" width="32" height="26" rx="2" fill="#f4e3cf" opacity=".35"/><rect x="34" y="52" width="32" height="32" rx="2" fill="#f4e3cf" opacity=".25"/>
<circle cx="64" cy="54" r="3" fill="url(#g-gold)" stroke="#8a6d1a"/>
<rect x="78" y="44" width="12" height="18" rx="2" fill="#3b424d"/><circle cx="84" cy="50" r="2" fill="#8fd16a"/>
"""
ICONS["browser"] = SHADOW + """
<rect x="8" y="16" width="84" height="66" rx="5" fill="#ffffff" stroke="#4a5562" stroke-width="1.6"/>
<path d="M8 21 a5 5 0 0 1 5 -5 h74 a5 5 0 0 1 5 5 v9 h-84 Z" fill="#d7dce2"/>
<circle cx="16" cy="23" r="2.4" fill="#e74c3c"/><circle cx="24" cy="23" r="2.4" fill="#f5b041"/><circle cx="32" cy="23" r="2.4" fill="#8fd16a"/>
<rect x="40" y="19.5" width="46" height="7" rx="3.5" fill="#ffffff" stroke="#9aa3ae" stroke-width=".8"/>
<rect x="16" y="38" width="40" height="7" rx="2" fill="#1f4e9c"/>
<g stroke="#b8c0ca" stroke-width="3.4" stroke-linecap="round"><line x1="16" y1="54" x2="84" y2="54"/><line x1="16" y1="63" x2="76" y2="63"/><line x1="16" y1="72" x2="64" y2="72"/></g>
"""

# ---- batch 4: people-facing attacks
ICONS["usb"] = SHADOW + """
<g transform="rotate(-35 50 50)">
<rect x="38" y="10" width="24" height="18" rx="2" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.2"/>
<rect x="43" y="15" width="5" height="5" fill="#3b424d"/><rect x="52" y="15" width="5" height="5" fill="#3b424d"/>
<rect x="32" y="28" width="36" height="58" rx="6" fill="#1f4e9c" stroke="#0d2c5c" stroke-width="1.4"/>
<rect x="38" y="44" width="24" height="26" rx="2" fill="#ffffff"/>
<text x="50" y="61" font-family="Helvetica, Arial, sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#c0392b">PAY</text></g>
"""
ICONS["trash"] = SHADOW + """
<path d="M22 34 h56 l-6 56 h-44 Z" fill="url(#g-green)" stroke="#1d5e22" stroke-width="1.4"/>
<rect x="16" y="26" width="68" height="10" rx="3" fill="#2e7d32" stroke="#1d5e22" stroke-width="1.2"/>
<g stroke="#1d5e22" stroke-width="2.4" opacity=".55"><line x1="38" y1="44" x2="40" y2="82"/><line x1="50" y1="44" x2="50" y2="82"/><line x1="62" y1="44" x2="60" y2="82"/></g>
<path d="M30 26 l4 -14 h22 l6 14" fill="url(#g-paper)" stroke="#9aa6b3" stroke-width="1"/>
<line x1="38" y1="18" x2="54" y2="18" stroke="#9aa6b3" stroke-width="2"/>
"""
ICONS["fingerprint"] = SHADOW + """
<g fill="none" stroke="#1f4e9c" stroke-width="3.2" stroke-linecap="round">
<path d="M30 30 a26 26 0 0 1 40 0"/><path d="M24 46 a26 26 0 0 1 52 0 v10"/><path d="M34 84 c-6 -10 -8 -22 -8 -32 a24 24 0 0 1 0 -2"/>
<path d="M36 52 a14 14 0 0 1 28 0 c0 14 -4 26 -10 36"/><path d="M50 52 c0 16 -4 28 -12 38"/><path d="M76 66 c-2 10 -6 18 -10 24"/></g>
"""
ICONS["money"] = SHADOW + """
<rect x="14" y="40" width="72" height="38" rx="4" fill="#5aa469" stroke="#1d5e22" stroke-width="1.2" transform="rotate(-8 50 59)"/>
<rect x="14" y="34" width="72" height="38" rx="4" fill="url(#g-green)" stroke="#1d5e22" stroke-width="1.4"/>
<circle cx="50" cy="53" r="11" fill="#e8f5e9" stroke="#1d5e22" stroke-width="1.2"/>
<text x="50" y="59" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#1d5e22">$</text>
<circle cx="24" cy="44" r="3" fill="#e8f5e9"/><circle cx="76" cy="62" r="3" fill="#e8f5e9"/>
"""
ICONS["videocall"] = SHADOW + """
<rect x="6" y="14" width="88" height="66" rx="5" fill="#2b3138" stroke="#14181d" stroke-width="1.4"/>
""" + "".join(f'<rect x="{10+(i%2)*42}" y="{18+(i//2)*29}" width="38" height="26" rx="2" fill="#4a5562"/>'
              f'<circle cx="{29+(i%2)*42}" cy="{27+(i//2)*29}" r="5.5" fill="url(#g-skin)"/>'
              f'<path d="M{19+(i%2)*42} {44+(i//2)*29} c0 -9 20 -9 20 0 Z" fill="{c}"/>' for i, c in enumerate(["#1f2d3d", "#6b3fa0", "#2e4a6b", "#7a4b2a"])) + """
<rect x="38" y="82" width="24" height="6" rx="2" fill="#9aa3ae"/>
"""
ICONS["fishhook"] = SHADOW + """
<path d="M54 10 v52 a16 16 0 0 1 -32 0 v-8" fill="none" stroke="#6b7785" stroke-width="5" stroke-linecap="round"/>
<path d="M22 50 l-6 10 l10 -2" fill="#6b7785"/><circle cx="54" cy="10" r="5" fill="none" stroke="#6b7785" stroke-width="3"/>
<rect x="56" y="34" width="34" height="24" rx="2" fill="#fff" stroke="#c0392b" stroke-width="1.6"/><path d="M56 34 l17 13 l17 -13" fill="none" stroke="#c0392b" stroke-width="1.6"/>
"""
ICONS["headset"] = SHADOW + """
<path d="M22 56 v-10 a28 28 0 0 1 56 0 v10" fill="none" stroke="#3b424d" stroke-width="5"/>
<rect x="14" y="50" width="16" height="26" rx="6" fill="#3b424d"/><rect x="70" y="50" width="16" height="26" rx="6" fill="#3b424d"/>
<path d="M78 74 q0 14 -20 16" fill="none" stroke="#3b424d" stroke-width="3"/><rect x="48" y="86" width="12" height="8" rx="3" fill="#1f4e9c"/>
<circle cx="50" cy="56" r="14" fill="url(#g-skin)"/><path d="M36 92 c0 -16 28 -16 28 0 Z" fill="#2e4a6b"/>
"""

# ---- batch 5: building and deception
ICONS["printer"] = SHADOW + """
<rect x="28" y="14" width="44" height="26" fill="url(#g-paper)" stroke="#6b7785" stroke-width="1.2"/>
<rect x="12" y="38" width="76" height="34" rx="5" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.4"/>
<rect x="24" y="62" width="52" height="26" fill="#ffffff" stroke="#6b7785" stroke-width="1.2"/>
<g stroke="#9aa6b3" stroke-width="2"><line x1="30" y1="70" x2="68" y2="70"/><line x1="30" y1="77" x2="60" y2="77"/></g>
<circle cx="78" cy="48" r="2.6" fill="#8fd16a"/>
"""
ICONS["camera"] = SHADOW + """
<rect x="10" y="22" width="12" height="12" rx="2" fill="#6b7785"/><path d="M16 34 v18 h14" fill="none" stroke="#6b7785" stroke-width="4"/>
<path d="M26 26 h50 l14 10 v14 l-14 10 h-50 Z" fill="url(#g-silver)" stroke="#5b6570" stroke-width="1.4"/>
<circle cx="80" cy="43" r="7" fill="#2b3138"/><circle cx="80" cy="43" r="3" fill="#4fc3f7"/>
<circle cx="34" cy="34" r="2.4" fill="#e74c3c"/>
"""
ICONS["honeypot"] = SHADOW + """
<path d="M30 30 q-18 10 -16 34 q2 26 36 26 q34 0 36 -26 q2 -24 -16 -34 Z" fill="url(#g-gold)" stroke="#8a6d1a" stroke-width="1.6"/>
<rect x="28" y="20" width="44" height="12" rx="4" fill="#b9770e" stroke="#7a4b12" stroke-width="1.2"/>
<path d="M36 32 q4 10 0 16 q-2 4 2 6" fill="none" stroke="#f9e79f" stroke-width="3" stroke-linecap="round"/>
<text x="50" y="72" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#7a4b12">HONEY</text>
"""
