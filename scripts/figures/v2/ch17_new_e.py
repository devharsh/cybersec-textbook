import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""


def level_card(p, x, y, w, h, n, title, defense, beaten, color):
    p.rect(x, y, w, h, "#ffffff", color, 2, rx=8, step=n)
    p.rect(x, y, 7, h, color, color, 1, rx=3, step=n)
    p.text(x + 40, y + 24, title, 14, color, "bold", anchor="start", step=n)
    p.text(x + 18, y + 48, defense, 12.5, INK, anchor="start", step=n)
    p.text(x + 18, y + 68, "beaten by: " + beaten, 12.5, RED, anchor="start", step=n)
    p.badge(n, x + 22, y + 19, step=n, color=color)


def gandalf_levels(name, title="How Gandalf's eight levels guard the password, and what beat each guard"):
    p = Fig(1180, 545, title,
            "A pipeline runs from the player's prompt through an input guard, then the model, whose system prompt holds the "
            "password, then an output guard, and back to the player. Cards under each stage show the levels that add a "
            "defense there. Level 1 has no rule and is beaten by asking. Level 2 tells the model not to reveal the password and "
            "is beaten by claiming authority or offering a wrong guess. Level 3 blocks replies that contain the password and is "
            "beaten by asking for it spelled out or encoded. Level 4 has a second model read the transcript and is beaten by "
            "descriptions and one letter at a time. Level 5 blocks prompts with the words password or secret and is beaten by "
            "another language or an abbreviation. Level 6 has a second model judge whether the prompt asks for the password and "
            "is beaten by indirect questions or a request to repeat the instructions. Level 7 combines everything and is beaten "
            "by combining techniques, such as an acrostic poem. Level 8, Gandalf the White, is updated from real attacks.")
    cy = 104
    p.icon("user", 70, cy, 52, "Player", "prompt", step=1, label_size=13)
    p.rect(214, cy - 36, 270, 72, "#fff8ee", ORANGE, 2, rx=10, step=1)
    p.text(349, cy - 6, "Input guard", 15, ORANGE, "bold", step=1)
    p.text(349, cy + 16, "checks the prompt", 12.5, INK, step=1)
    p.rect(504, cy - 36, 270, 72, "#eef5fc", BLUE, 2, rx=10, step=1)
    p.icon("robot", 540, cy, 40, step=1)
    p.text(660, cy - 6, "Model", 15, BLUE, "bold", step=1)
    p.text(660, cy + 16, "system prompt holds it", 12.5, INK, step=1)
    p.rect(794, cy - 36, 270, 72, "#f7f2fb", PURPLE, 2, rx=10, step=1)
    p.text(929, cy - 6, "Output guard", 15, PURPLE, "bold", step=1)
    p.text(929, cy + 16, "checks the reply", 12.5, INK, step=1)
    p.arrow([(100, cy), (210, cy)], None, INK, step=1)
    p.arrow([(484, cy), (500, cy)], None, INK, step=1, width=1.8)
    p.arrow([(774, cy), (790, cy)], None, INK, step=1, width=1.8)
    p.arrow([(1064, cy), (1110, cy)], None, INK, step=1)
    p.icon("document", 1134, cy, 40, "Reply", None, step=1, label_size=13)
    w, h = 270, 84
    level_card(p, 504, 168, w, h, 1, "Level 1: no rule", "the prompt just states the password", "asking for it", BLUE)
    level_card(p, 504, 264, w, h, 2, "Level 2: do not reveal it", "a rule in the system prompt", "claimed authority, a wrong guess", BLUE)
    level_card(p, 794, 168, w, h, 3, "Level 3: string match", "block replies that contain it", "spell it, encode it", PURPLE)
    level_card(p, 794, 264, w, h, 4, "Level 4: LLM judge", "a second model reads the transcript", "describe it, one letter at a time", PURPLE)
    level_card(p, 214, 168, w, h, 5, "Level 5: word list", "block password and secret", "another language, pw", ORANGE)
    level_card(p, 214, 264, w, h, 6, "Level 6: LLM classifier", "is the prompt asking for it?", "indirect questions, repeat rules", ORANGE)
    level_card(p, 214, 372, 560, h, 7, "Level 7: everything at once", "word lists and LLM checks on both the prompt and the reply",
               "combined tricks, such as an acrostic poem", GREEN)
    level_card(p, 794, 372, 270, h, 8, "Level 8: Gandalf the White", "updated from real attacks", "rare; slow, indirect, multi-turn", RED)
    for x in (349, 929):
        p.raw(f'<line x1="{x}" y1="{cy+36}" x2="{x}" y2="166" stroke="#b8c2cc" stroke-width="2" stroke-dasharray="4 4"/>', step=1)
    p.raw(f'<line x1="639" y1="{cy+36}" x2="639" y2="166" stroke="#b8c2cc" stroke-width="2" stroke-dasharray="4 4"/>', step=1)
    p.text(590, 500, "Each level adds one defense; the badge on each card is its level number.", 13, MUTED)
    p.text(590, 520, "The techniques are families, not magic strings: the same idea works with many different wordings.", 13, MUTED)
    p.save(OUT + name)


if __name__ == "__main__":
    gandalf_levels("ch17_gandalf_levels")
