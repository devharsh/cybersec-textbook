import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch04.pkl","rb")); A=C.append

A(md(r'''## 4.4 The Taxonomy of Social-Engineering Attacks

With the lifecycle and psychology established, we can name the specific techniques an attacker deploys.
They divide naturally into those conducted at a distance, through technology, and those conducted in
person.

The largest family is **phishing** and its variants. Plain **phishing** casts a wide net, sending
fraudulent messages (usually email) to many recipients hoping some will reveal credentials, send money,
or run malware. **Spear phishing** is targeted: the attacker researches a specific person or group and
crafts a personalized message referencing their employer, colleagues, or projects, which makes it far
more convincing. **Whaling** targets the biggest fish, executives and other high-value individuals, where
a single success yields outsized returns; a common form is business email compromise, in which an
attacker impersonates a CEO to authorize a fraudulent wire transfer. **Vishing (voice phishing)** moves
the attack to the phone, where tone of voice conveys authority and urgency convincingly. **Smishing (SMS
phishing)** uses text messages, often with a link to a fake login page. **Pharming** is more technical:
rather than luring a victim with a link, it redirects them from a legitimate website to a fraudulent one,
typically by tampering with DNS, so that even a careful user who types the correct address is sent to the
attacker.

Other distance techniques include **pretexting**, inventing a believable scenario (for example posing as
an auditor or a new employee) to justify a request, and **baiting**, leaving malware-laden media such as
a USB drive labeled "Payroll" where a curious victim will find and use it. **Quid pro quo** offers a
service in exchange for information, such as a fake IT technician offering to fix a problem if the user
provides their password. **Reverse social engineering** is subtler: the attacker first creates a problem
(for example by sabotaging equipment), then poses as the helper who can fix it, so the victim
*initiates* contact and willingly grants access.

In-person techniques exploit physical presence. **Tailgating** is following an authorized person through
a secure door without their knowledge (for instance slipping in behind them), while **piggybacking** is
the same but with their consent, often gained by carrying boxes or feigning a lost badge. **Dumpster
diving** recovers sensitive documents, password notes, and discarded media from the trash, and **shoulder
surfing** is simply watching someone enter a password or personal identification number (PIN). The
diagram summarizes the phishing family.

```{mermaid}
graph TD
    P[Phishing - fraudulent messages] --> SP[Spear phishing - targeted]
    SP --> W[Whaling - executives / CEO fraud]
    P --> V[Vishing - voice / phone]
    P --> S[Smishing - SMS text]
    P --> PH[Pharming - DNS redirection]
```

```{admonition} Knowledge Check
:class: hint
1. What distinguishes spear phishing from ordinary phishing?
2. A worker props open a secure door for a stranger carrying coffee in both hands. Is this tailgating or
   piggybacking?

*Answers:* (1) Spear phishing is personalized and aimed at a specific individual or group using
researched details, whereas ordinary phishing is generic and sent broadly. (2) Piggybacking, because the
authorized worker knowingly granted access; tailgating would be entering without that person's awareness.
```
'''))

A(md(r'''## 4.5 Vectors and the Role of Open-Source Intelligence

The techniques above reach victims through several channels, and modern attackers blend them. **Email**
remains the dominant vector, carrying phishing links and malicious attachments. The **telephone** powers
vishing and help-desk impersonation. **Text messages and messaging apps** carry smishing.
**Social-networking sites** are doubly dangerous: attackers impersonate trusted contacts to reach a
victim's network, and they harvest the personal details that make spear phishing convincing. **Websites
and pop-ups** present fake login prompts and fraudulent "your account needs attention" pages, and
**removable media** delivers baiting payloads.

What ties these vectors together is reconnaissance, and specifically **open-source intelligence
(OSINT)**, the gathering of information from publicly available sources. Before a convincing pretext can
be built, the attacker needs raw material, and people supply it freely. Job postings reveal the
technologies a company uses; employee social-media profiles reveal names, roles, schedules, and
relationships; conference talks and press releases reveal projects and vendors. A particularly
underappreciated source is **location data and geotagging**: most smartphones embed geographic
coordinates in photos by default, and when such a photo is posted publicly, it can reveal exactly where a
person lives, works, or travels. Cellular networks can likewise locate a phone by triangulating its
signal among towers. This connection between social engineering and reconnaissance is so important that
Chapter 7 is devoted to reconnaissance as a discipline; here the lesson is that the personal information
people scatter across the internet is the fuel for targeted social engineering, and that limiting it,
through privacy settings, careful posting, and organizational policy, directly shrinks the attacker's
opportunity.
'''))

A(md(r'''## 4.6 Recognizing and Analyzing Phishing

Because phishing is the most common social-engineering attack, the ability to recognize it is the single
most valuable defensive skill for an ordinary user, so we devote a section to it before turning to
physical attacks. Phishing messages share recurring tells. The **sender address** often does not match
the organization it claims to represent, using a look-alike domain or a public mailbox. The message may
contain **poor grammar or spelling**, though well-funded campaigns increasingly do not. It typically
**creates urgency or fear**, demanding immediate action to avoid a consequence. It **requests sensitive
information** or credentials that a legitimate organization would never ask for by email. Its **links**,
when hovered over without clicking, reveal a destination that differs from the displayed text or the
purported sender. And it may carry an **unexpected attachment** that the recipient is pressed to open.

The practical defensive habit is to slow down and verify through an independent channel: rather than
clicking a link or calling a number in the message, navigate to the organization's known website or call
its published number. Hovering over links to inspect the true destination, checking the full sender
address, and treating any urgent request for credentials or money as suspicious until verified will
defeat the great majority of phishing. The code cell below models this reasoning as a simple,
explainable indicator checker, the kind of logic email-security gateways apply at scale.
'''))

A(code(r'''# Chapter 4 -- A simple, explainable phishing-indicator checker (educational)
import re

def phishing_score(sender, subject, body, claimed_org_domain):
    flags = []
    # 1. Sender domain mismatch
    m = re.search(r"@([\w.-]+)", sender)
    sender_domain = m.group(1).lower() if m else ""
    if claimed_org_domain.lower() not in sender_domain:
        flags.append(f"Sender domain '{sender_domain}' does not match '{claimed_org_domain}'")
    # 2. Urgency / fear language
    urgent = ["urgent","immediately","within 24 hours","account.*suspend","verify now","act now","final notice"]
    if any(re.search(w, (subject+" "+body).lower()) for w in urgent):
        flags.append("Creates urgency or fear")
    # 3. Requests credentials / sensitive info
    if re.search(r"password|ssn|social security|credit card|login|one-time code|otp", body.lower()):
        flags.append("Requests sensitive information")
    # 4. Mismatched link (display text vs href)
    for disp, href in re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", body):
        if "." in disp and disp.split("/")[0] not in href:
            flags.append(f"Link text '{disp}' hides real destination '{href}'")
    # 5. Generic greeting
    if re.search(r"dear (customer|user|account holder|sir/madam)", body.lower()):
        flags.append("Generic, impersonal greeting")
    verdict = "LIKELY PHISHING" if len(flags) >= 2 else "Lower risk (still verify)"
    return verdict, flags

sender  = "security@paypa1-support.com"
subject = "Urgent: verify your account immediately"
body    = ("Dear customer, we lost your network connection and your account will be suspended. "
           "Please confirm your password and one-time code at "
           "[paypal.com/verify](http://paypa1-support.com/login) within 24 hours.")
verdict, flags = phishing_score(sender, subject, body, "paypal.com")
print("Verdict:", verdict)
for f in flags:
    print("  flag:", f)''' ))

A(md(r'''```{admonition} In-Class Exercise: dissect a phish
:class: note
Working in pairs, take a real phishing email (use one from your spam folder or a sample from a public
phishing-awareness archive, never a live malicious link) and annotate every indicator you can find: the
true sender address, mismatched or disguised links (hover, do not click), urgency or fear language,
spelling and grammar errors, requests for sensitive data, and the impersonated brand. Then rewrite the
message as the legitimate organization would have written it, and list the steps the recipient should
take to verify it through an independent channel. Present your annotated phish to the class. Do not click
any links or open any attachments during this exercise.
```
'''))
print("part B:", len(C))
pickle.dump(C, open(".build/_ch04.pkl","wb"))
