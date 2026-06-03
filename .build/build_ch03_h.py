import sys, json, uuid; sys.path.insert(0,".build")
path="chapters/03_networking/chapter03.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 3.5", r'''

### Application Protocols and Their Security Posture

Knowing a port is open is only useful if you know what the service behind it does and how it fails, so
this subsection pairs the most common protocols with their security posture. **HTTP (port 80)** carries
web traffic in cleartext and should be replaced by **HTTPS (port 443)**, which wraps HTTP in TLS;
unencrypted HTTP exposes credentials and session cookies to the sniffing of Section 3.8. **FTP (ports 20
and 21)** and **TFTP (port 69)** transfer files in cleartext, including passwords, and are superseded by
SFTP/FTPS and secure alternatives. **Telnet (port 23)** provides remote login in cleartext and is one of
the most dangerous services to find exposed; **SSH (port 22)** is its encrypted replacement. **SMTP
(port 25)** moves email and, in its original form, neither encrypts nor authenticates, which is why email
security relies on added layers (STARTTLS, plus SPF, DKIM, and DMARC for authentication, discussed in
Chapter 4). **SNMP (ports 161 and 162)** manages network devices and, in early versions with default
community strings such as "public," leaks extensive information; only SNMPv3 offers strong security.
**SMB (port 445)** provides Windows file sharing and has been the vector for major worms (the EternalBlue
exploit behind WannaCry targeted SMB), so it should never be exposed to the internet. **LDAP (port 389)**
queries directory services and should be secured with LDAPS. **RDP (port 3389)** provides remote desktop
access and is a leading ransomware entry point when exposed, so it belongs behind a VPN. The lesson is a
direct extension of Chapter 1's attack-surface principle: every open port is a service, every legacy
cleartext service is a liability, and a core hardening task is to replace insecure protocols with their
encrypted equivalents and to close everything not needed.

```{admonition} Knowledge Check
:class: hint
1. A scan finds TCP 23 and TCP 22 both open on a server. Which should concern you more, and why?
2. Why is finding SNMP with the community string "public" a serious issue?

*Answers:* (1) Port 23 (Telnet) is the concern: it transmits credentials and commands in cleartext, so
anyone sniffing can capture the login; SSH on 22 is encrypted and is the safe replacement. (2) A default
"public" community string often allows an attacker to read detailed device and network configuration
information, aiding reconnaissance and further attack.
```''')

app("## 3.4", r'''

IPv6 deserves a specific security note because its rollout creates blind spots. Since IPv6 is enabled by
default on modern operating systems, a network that is monitored and filtered only for IPv4 may have a
completely unguarded IPv6 path running in parallel, over which attackers can communicate or exfiltrate
data unnoticed. IPv6 also changes familiar mechanics: it replaces ARP with the Neighbor Discovery
Protocol (NDP), which has its own spoofing risks analogous to ARP poisoning, and its vast address space
makes traditional sweep scanning impractical while making other discovery techniques (such as leveraging
DNS and multicast) more important. The practical guidance is to secure, monitor, and filter IPv6 with the
same rigor as IPv4, or to disable it deliberately where it is genuinely not needed, rather than leaving
it on and ignored.''')

app("## 3.8", r'''

### Wireless Networking Fundamentals

Because so much traffic now travels over radio rather than copper or fiber, a security professional needs
a working grasp of wireless networking, whose depth is developed in Chapter 16. Wi-Fi is standardized by
the IEEE 802.11 family, in which an *access point* advertises a network name (the Service Set Identifier,
or SSID) and clients associate to it. The defining property is that the medium is *shared radio*: anyone
within range can receive the frames, so link-layer encryption is the only thing standing between a
passive listener and the traffic. The history of that encryption is a cautionary tale. **WEP (Wired
Equivalent Privacy)** was the original scheme and is fatally broken, recoverable in minutes because of
flaws in how it used its cipher and initialization vectors. **WPA and WPA2 (Wi-Fi Protected Access)**
replaced it, with WPA2's AES-based encryption remaining secure when paired with a strong passphrase,
though weak passphrases fall to offline dictionary attacks after an attacker captures the handshake.
**WPA3** further hardens the key exchange against such offline guessing. Beyond cracking encryption,
wireless introduces distinctive attacks: the *evil twin*, a rogue access point impersonating a legitimate
SSID to lure victims; *deauthentication* attacks that forcibly disconnect clients (often to capture the
reconnection handshake); and attacks on the convenience feature Wi-Fi Protected Setup (WPS). The enduring
defense is the same one this chapter repeats: never rely on the wireless layer alone, and ensure
sensitive traffic carries its own end-to-end encryption so that even a fully compromised wireless link
yields only ciphertext.''')

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter03: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
