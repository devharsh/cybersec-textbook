import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""


def art50_vs_art15(name, gen_label="Generator", gen_icon="gear", mark_sub="watermark + metadata",
                   bot_label="Chatbot", model_label="Model"):
    p = Fig(1180, 704, "Article 50 versus Article 15: transparency versus accuracy, robustness, and cybersecurity",
            "The top lane shows the four Article 50 duties, which apply at any risk level from August 2, 2026. A provider's "
            "chatbot tells the person that it is an AI system. A provider's generator marks its output in a machine-readable "
            "way so a detector can recognize it. A deployer of emotion recognition informs the people exposed to it. A deployer "
            "that publishes a deepfake labels it as AI-generated. The bottom lane shows Article 15, which applies only to "
            "high-risk systems: the provider declares accuracy levels and metrics in the instructions for use, builds in "
            "redundancy and a fail-safe so faults do not cause harm, protects the model against data poisoning and "
            "adversarial inputs, and shows all of this in a conformity assessment before the system is placed on the market.")
    O = 44
    # Lane A: Article 50
    p.zone(20, 20 + O, 1140, 292, "Article 50: tell people about AI and mark AI output", BLUE, "#eef5fc")
    p.text(34, 62 + O, "Providers and deployers, at any risk level. Applies from August 2, 2026.", 13, MUTED, anchor="start")
    cy = 160 + O
    # 1 interaction disclosure
    p.icon("bot", 100, cy, 62, bot_label, None, step=1, label_size=14)
    p.arrow([(134, cy), (228, cy)], "told it is AI", BLUE, step=1, size=12)
    p.icon("user", 262, cy, 56, "Person", None, step=1, label_size=14)
    p.badge(1, 56, 104 + O, step=1)
    p.text(170, 262 + O, "50(1) Provider", 14, BLUE, "bold", step=1)
    p.text(170, 281 + O, "discloses the interaction", 13, INK, step=1)
    # 2 machine-readable marking and detection
    p.icon(gen_icon, 360, cy, 56, gen_label, None, step=2, label_size=14)
    p.arrow([(390, cy), (432, cy)], None, BLUE, step=2)
    p.icon("document", 462, cy, 56, "Output", mark_sub, step=2, label_size=14)
    p.icon("fingerprint", 482, cy + 14, 24, step=2)
    p.arrow([(492, cy), (526, cy)], None, BLUE, step=2)
    p.icon("search", 558, cy, 56, "Detector", None, step=2, label_size=14)
    p.badge(2, 336, 104 + O, step=2)
    p.text(450, 262 + O, "50(2) Provider", 14, BLUE, "bold", step=2)
    p.text(450, 281 + O, "marks output, keeps it detectable", 13, INK, step=2)
    # 3 emotion recognition and biometric categorization
    p.icon("eye", 680, cy, 56, "Emotion", "recognition", step=3, label_size=14)
    p.arrow([(712, cy), (788, cy)], "informed", BLUE, step=3, size=12)
    p.icon("user", 820, cy, 56, "Person", None, step=3, label_size=14)
    p.badge(3, 616, 104 + O, step=3)
    p.text(730, 262 + O, "50(3) Deployer", 14, BLUE, "bold", step=3)
    p.text(730, 281 + O, "informs the people exposed", 13, INK, step=3)
    # 4 deepfake and public-interest text disclosure
    p.icon("videocall", 940, cy, 60, "Deepfake", None, step=4, label_size=14)
    p.rect(896, 104 + O, 88, 22, "#fdecea", RED, 1.6, rx=5, step=4)
    p.text(940, 120 + O, "AI-generated", 12, RED, "bold", step=4)
    p.arrow([(974, cy), (1066, cy)], "labeled", BLUE, step=4, size=12)
    p.icon("group", 1100, cy, 58, "Public", None, step=4, label_size=14)
    p.badge(4, 868, 104 + O, step=4)
    p.text(1010, 262 + O, "50(4) Deployer", 14, BLUE, "bold", step=4)
    p.text(1010, 281 + O, "discloses deepfakes and public-interest text", 13, INK, step=4)

    # Lane B: Article 15
    p.zone(20, 332 + O, 1140, 308, "Article 15: build a high-risk system to work well and resist attack", PURPLE, "#f7f2fb")
    p.text(34, 374 + O, "The provider, high-risk systems only. Applies from December 2, 2027 (Annex III) and August 2, 2028 (Annex I).",
           13, MUTED, anchor="start")
    cy = 478 + O
    # 5 accuracy declared
    p.icon("checklist", 96, cy, 58, "Instructions", "for use", step=5, label_size=14)
    p.rect(150, cy - 30, 130, 58, "#ffffff", PURPLE, 1.5, rx=6, step=5)
    p.text(215, cy - 8, "accuracy level", 12.5, INK, step=5)
    p.text(215, cy + 14, "metric used", 12.5, INK, step=5)
    p.badge(5, 56, 420 + O, step=5, color=PURPLE)
    p.text(170, 590 + O, "15(1) to 15(3) Accuracy", 14, PURPLE, "bold", step=5)
    p.text(170, 609 + O, "levels and metrics declared", 13, INK, step=5)
    # 6 robustness: redundancy and fail-safe
    p.icon("server", 370, cy, 58, "Primary", None, step=6, label_size=14)
    p.arrow([(402, cy), (500, cy)], "on fault", PURPLE, step=6, size=12, dash=True)
    p.icon("rack", 532, cy, 56, "Fail-safe", "backup", step=6, label_size=14)
    p.badge(6, 336, 420 + O, step=6, color=PURPLE)
    p.text(450, 590 + O, "15(4) Robustness", 14, PURPLE, "bold", step=6)
    p.text(450, 609 + O, "redundancy, fail-safe, feedback loops", 13, INK, step=6)
    # 7 cybersecurity against AI-specific attacks
    p.text(706, 416 + O, "data poisoning,", 12.5, RED, "bold", step=7)
    p.text(706, 432 + O, "adversarial inputs", 12.5, RED, "bold", step=7)
    p.icon("attacker", 648, cy, 54, "Attacker", None, step=7, label_size=14, label_color=RED)
    p.arrow([(678, cy), (732, cy)], None, RED, step=7)
    p.icon("shield", 762, cy, 56, None, None, step=7)
    p.icon("robot", 826, cy, 56, model_label, None, step=7, label_size=14)
    p.badge(7, 616, 420 + O, step=7, color=PURPLE)
    p.text(730, 590 + O, "15(5) Cybersecurity", 14, PURPLE, "bold", step=7)
    p.text(730, 609 + O, "resists AI-specific attacks", 13, INK, step=7)
    # 8 conformity assessment before the market
    p.icon("certificate", 944, cy, 58, "Conformity", "assessment", step=8, label_size=14)
    p.arrow([(978, cy), (1060, cy)], None, GREEN, step=8)
    p.icon("check", 1096, cy, 44, "On the market", None, step=8, label_size=14, label_color=GREEN)
    p.badge(8, 868, 420 + O, step=8, color=PURPLE)
    p.text(1010, 590 + O, "Provider shows compliance", 14, PURPLE, "bold", step=8)
    p.text(1010, 609 + O, "Articles 16 and 43", 13, INK, step=8)
    p.save(OUT + name)


if __name__ == "__main__":
    art50_vs_art15("ch17_art50_vs_art15")
