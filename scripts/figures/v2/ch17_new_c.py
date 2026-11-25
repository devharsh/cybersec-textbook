import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Build provenance with in-toto and SLSA: the artifact lane and the evidence lane
p = Fig(1180, 600, "Build provenance: the platform records how the artifact was made, and the gate checks it",
        "A source repository at tag v1.4 feeds a hardened build platform. The platform outputs the model file with its SHA-256 digest "
        "and an in-toto Statement whose SLSA provenance predicate names the subject digest, the builder, the source and ref, and the "
        "resolved dependencies. The platform signs the statement inside a DSSE envelope with a key that build steps cannot reach. "
        "The registry stores the artifact and the attestation together. A deployment gate admits the model only if a trusted builder "
        "signed, the digest matches a subject, and the source and parameters are the expected ones; a swapped file, an unknown "
        "builder, or a build from a fork is refused.")
# 1 source
p.icon("code", 90, 200, 66, "Source repository", "tag v1.4, commit 3f1c9a7", step=1, label_size=14)
p.badge(1, 46, 150, step=1)
# 2 build platform
p.arrow([(132, 200), (252, 200)], None, INK, step=2)
p.icon("server", 290, 200, 76, "Hardened build platform", "isolated runs", step=2, label_size=14)
p.badge(2, 238, 146, step=2)
# 3 artifact lane
p.arrow([(332, 176), (470, 120)], "artifact", BLUE, step=3, size=12)
p.icon("document", 530, 112, 56, "model.safetensors", "sha256 9b2e...41", step=3, label_size=14)
p.badge(3, 490, 78, step=3)
# 4 evidence lane: the in-toto Statement with the SLSA provenance predicate
p.arrow([(300, 290), (414, 372)], None, PURPLE, step=4)
p.text(356, 346, "evidence", 12, PURPLE, "bold", "end", step=4)
p.rect(424, 300, 262, 176, "#f7f2fb", PURPLE, 1.8, rx=10, step=4)
p.text(555, 324, "in-toto Statement", 14, PURPLE, "bold", step=4)
for i, line in enumerate(["subject: model.safetensors + sha256", "predicateType: SLSA provenance v1",
                          "builder.id: ci.example.com/hardened", "source: models repo at v1.4",
                          "dependencies: base model, tools"]):
    p.text(438, 350 + i * 24, line, 12.5, INK, anchor="start", step=4)
p.badge(4, 424, 300, step=4, color=PURPLE)
# 5 DSSE envelope around the statement, signed with the platform key
p.rect(404, 270, 302, 230, "none", PURPLE, 2.2, rx=14, step=5, dash=True)
p.icon("key", 690, 284, 40, step=5)
p.badge(5, 414, 518, step=5, color=PURPLE)
p.text(434, 523, "DSSE envelope: signed over PAE(type, statement)", 12.5, PURPLE, "bold", "start", step=5)
p.text(434, 543, "by a key the build steps cannot reach", 12.5, INK, anchor="start", step=5)
# 6 registry keeps the artifact and its attestation together
p.text(772, 168, "Registry", 14, INK, "bold", step=6)
p.text(772, 186, "artifact + attestation", 12.5, MUTED, step=6)
p.icon("database", 772, 232, 62, step=6)
p.arrow([(562, 112), (730, 214)], None, BLUE, step=6)
p.arrow([(706, 400), (772, 400), (772, 272)], None, PURPLE, step=6)
p.badge(6, 734, 262, step=6)
# 7 deployment gate
p.arrow([(808, 232), (856, 232)], None, INK, step=7)
p.icon("shield", 900, 230, 70, "Deployment gate", None, step=7, label_size=14)
for i, line in enumerate(["trusted builder signed it", "digest matches a subject", "source and ref as expected"]):
    p.icon("check", 976, 199 + i * 26, 18, step=7)
    p.text(990, 204 + i * 26, line, 12.5, INK, anchor="start", step=7)
p.badge(7, 858, 186, step=7)
# 8 admit, 9 refuse
p.arrow([(935, 196), (1072, 112)], None, GREEN, step=8)
p.text(990, 146, "admit", 12, GREEN, "bold", "end", step=8)
p.icon("server", 1110, 96, 56, "Production", None, step=8, label_size=13, label_color=GREEN)
p.badge(8, 1074, 62, step=8, color=GREEN)
p.arrow([(980, 266), (1090, 398)], None, RED, step=9)
p.text(1040, 318, "refuse", 12, RED, "bold", "start", step=9)
p.icon("cross", 1110, 420, 44, "Refused", None, step=9, label_size=13, label_color=RED)
p.text(1110, 478, "swapped file,", 12, INK, step=9)
p.text(1110, 494, "unknown builder,", 12, INK, step=9)
p.text(1110, 510, "or fork build", 12, INK, step=9)
p.badge(9, 1150, 402, step=9, color=RED)
p.save(OUT + "ch17_build_provenance")
