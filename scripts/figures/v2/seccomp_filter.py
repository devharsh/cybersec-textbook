import os
"""Seccomp: how a syscall filter sits between a process and the kernel, and how profiles are applied.
One drawing, two label sets: the cybersecurity book (ch17) and the Bedrock book (bk)."""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch17_seccomp_filter": {
        "title": "Seccomp: a system call filter in front of the kernel",
        "proc": ("Model server process", ["normal: read, futex, sendto", "attacker: unshare, mount"]),
        "layers_title": "A layer, not a sandbox",
        "layers": [("idcard", "Drop capabilities; set no_new_privs"), ("shield", "AppArmor or SELinux for files"),
                   ("firewall", "Network policy for egress"), ("rack", "gVisor or a microVM for untrusted code")]},
    "bk_seccomp_filter": {
        "title": "Seccomp for model servers and agent tools on AWS",
        "proc": ("Model server or tool sandbox", ["normal: read, futex, sendto", "attacker: unshare, mount"]),
        "layers_title": "Who sets the filter on AWS",
        "layers": [("cloud", "AgentCore: a microVM per session"), ("rack", "Firecracker filters its own VMM"),
                   ("server", "EKS on EC2: you set the profile"), ("gear", "ECS on Fargate: AWS runs the runtime")]},
}

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 560, L["title"],
            "Step 1, a process such as a model server makes system calls, some normal and some from injected "
            "attacker code. Step 2, the seccomp filter, a small BPF program, checks each call's number and raw "
            "argument values but cannot follow pointers to read paths or buffers. Step 3, allowed calls run in the "
            "kernel. Step 4, denied calls fail with an error or kill the process. Step 5, a profile is built by "
            "recording a test run in log mode, then allowing only the recorded calls and denying the rest. Step 6, "
            "Kubernetes offers three profile types: RuntimeDefault, the runtime's default; Localhost, a custom file "
            "on the node; and Unconfined, no filter, which is the Kubernetes default unless the kubelet's "
            "seccomp-default setting is on. Step 7 shows the other layers that seccomp works with.")
    Y0, H = 52, 236
    # 1 process
    p.rect(18, Y0, 236, H, "#eef5fc", BLUE, 2, rx=14, step=1)
    p.icon("robot", 136, Y0 + 58, 56, step=1)
    p.text(136, Y0 + 124, L["proc"][0], 14, INK, "bold", step=1)
    p.text(136, Y0 + 152, L["proc"][1][0], 12, GREEN, step=1)
    p.text(136, Y0 + 172, L["proc"][1][1], 12, RED, step=1)
    p.text(136, Y0 + 204, "every call goes through", 12, MUTED, step=1)
    p.text(136, Y0 + 220, "the filter first", 12, MUTED, step=1)
    p.badge(1, 234, Y0 + 20, step=1, color=BLUE)
    p.arrow([(256, Y0 + H / 2), (290, Y0 + H / 2)], color=INK, step=2, width=2.2)
    # 2 filter
    p.rect(292, Y0, 270, H, "#fff4e8", ORANGE, 2, rx=14, step=2)
    p.icon("shield", 427, Y0 + 58, 56, step=2)
    p.text(427, Y0 + 124, "seccomp filter (BPF)", 14, INK, "bold", step=2)
    p.text(427, Y0 + 152, "checks the syscall number", 12, MUTED, step=2)
    p.text(427, Y0 + 170, "and raw argument values", 12, MUTED, step=2)
    p.text(427, Y0 + 196, "cannot follow pointers,", 12, ORANGE, "bold", step=2)
    p.text(427, Y0 + 214, "so it never sees a path", 12, ORANGE, "bold", step=2)
    p.badge(2, 542, Y0 + 20, step=2, color=ORANGE)
    # 3 allow -> kernel, 4 deny -> error
    p.arrow([(564, Y0 + 70), (600, Y0 + 56)], color=GREEN, step=3, width=2.2)
    p.rect(602, Y0, 300, 108, "#edf7ee", GREEN, 2, rx=12, step=3)
    p.icon("server", 646, Y0 + 54, 46, step=3)
    p.text(680, Y0 + 44, "Allowed: runs in the kernel", 13.5, INK, "bold", anchor="start", step=3)
    p.text(680, Y0 + 66, "read, futex, sendto, and", 12, MUTED, anchor="start", step=3)
    p.text(680, Y0 + 84, "thread-only clone calls", 12, MUTED, anchor="start", step=3)
    p.badge(3, 882, Y0 + 20, step=3, color=GREEN)
    p.arrow([(564, Y0 + 166), (600, Y0 + 180)], color=RED, step=4, width=2.2)
    p.rect(602, Y0 + 128, 300, 108, "#fdeeee", RED, 2, rx=12, step=4)
    p.icon("cross", 646, Y0 + 182, 40, step=4)
    p.text(680, Y0 + 172, "Denied: error or kill", 13.5, INK, "bold", anchor="start", step=4)
    p.text(680, Y0 + 194, "EPERM back to the caller,", 12, MUTED, anchor="start", step=4)
    p.text(680, Y0 + 212, "or the process is killed", 12, MUTED, anchor="start", step=4)
    p.badge(4, 882, Y0 + 148, step=4, color=RED)
    # 5 build the profile
    p.rect(924, Y0, 238, H, "#f3eef9", PURPLE, 2, rx=14, step=5)
    p.icon("checklist", 1043, Y0 + 58, 52, step=5)
    p.text(1043, Y0 + 124, "Build the profile", 14, INK, "bold", step=5)
    for k, t in enumerate(["record a test run in log mode", "allow only the recorded calls",
                           "deny everything else", "rerun after every upgrade"]):
        p.text(1043, Y0 + 152 + k * 19, t, 12, MUTED, step=5)
    p.badge(5, 1142, Y0 + 20, step=5, color=PURPLE)
    # 6 Kubernetes profile types
    zy = 312
    p.zone(18, zy, 560, 230, "Kubernetes seccompProfile types", color=INK, fill="#f6f7f9", step=6)
    rows = [("check", "RuntimeDefault", "the container runtime's default profile"),
            ("check", "Localhost", "your JSON file under /var/lib/kubelet/seccomp"),
            ("cross", "Unconfined", "no filter; the default unless the kubelet's"),]
    for k, (ic, h, s) in enumerate(rows):
        yy = zy + 64 + k * 52
        p.icon(ic, 52, yy, 30, step=6)
        p.text(80, yy - 6, h, 13.5, INK, "bold", anchor="start", step=6)
        p.text(80, yy + 12, s, 12, MUTED, anchor="start", step=6)
    p.text(80, zy + 64 + 2 * 52 + 28, "seccomp-default setting is on", 12, MUTED, anchor="start", step=6)
    p.text(298, zy + 216, "privileged containers always run Unconfined", 12, RED, "bold", step=6)
    p.badge(6, 558, zy + 20, step=6, color=INK)
    # 7 layers
    p.zone(602, zy, 560, 230, L["layers_title"], color=INK, fill="#f6f7f9", step=7)
    for k, (ic, t) in enumerate(L["layers"]):
        yy = zy + 64 + k * 42
        p.icon(ic, 640, yy, 30, step=7)
        p.text(668, yy + 5, t, 13, INK, anchor="start", step=7)
    p.badge(7, 1142, zy + 20, step=7, color=INK)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
