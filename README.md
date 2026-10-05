# Cybersecurity: Theory, Practice, and Ethics

An open, executable textbook for university-level cybersecurity education.

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20575785-blue)](https://doi.org/10.5281/zenodo.20575785)

**Live at:** https://book.com.puter.tips

**DOI:** https://doi.org/10.5281/zenodo.20575785


## Contents

20 chapters covering foundations, ethical hacking, network defense, digital
forensics, incident response, malware analysis, privacy law, governance, and
industrial control system security. Each chapter includes learning objectives,
worked code examples, 10 review questions, and a lab assignment.

## Courses supported

- Introduction to IT Security
- Ethical Hacking
- Computer and Network Security
- Fundamentals of Cryptography
- Incident Response and Digital Forensics
- Cybersecurity and Society

## How to cite

If you use this textbook in research, teaching, or writing, please cite it by its DOI,
[10.5281/zenodo.20575785](https://doi.org/10.5281/zenodo.20575785). This is the Zenodo concept DOI, which
always resolves to the newest release. To cite one exact release, use that release's own DOI instead; the
current release, version 1.1.1 of June 7, 2026, is
[10.5281/zenodo.20581926](https://doi.org/10.5281/zenodo.20581926). The website at
https://book.com.puter.tips is updated continuously, so when you cite material from it, add the date you
accessed it.

**APA (7th edition)**

> Trivedi, D. (2026). *Cybersecurity: Theory, practice, and ethics*. Zenodo. https://doi.org/10.5281/zenodo.20575785

**IEEE**

> D. Trivedi, *Cybersecurity: Theory, Practice, and Ethics*. Zenodo, 2026. doi: 10.5281/zenodo.20575785.

**MLA (9th edition)**

> Trivedi, Devharsh. *Cybersecurity: Theory, Practice, and Ethics*. Zenodo, 2026, https://doi.org/10.5281/zenodo.20575785.

**Chicago (author-date)**

> Trivedi, Devharsh. 2026. *Cybersecurity: Theory, Practice, and Ethics*. Zenodo. https://doi.org/10.5281/zenodo.20575785.

**BibTeX**

```bibtex
@book{trivedi2026cybersecurity,
  author    = {Trivedi, Devharsh},
  title     = {{Cybersecurity: Theory, Practice, and Ethics}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20575785},
  url       = {https://doi.org/10.5281/zenodo.20575785},
  note      = {Free, open-source textbook, CC BY 4.0}
}
```

To point to a single chapter, cite the whole book and name the chapter where you cite it, for example
(Trivedi, 2026, Chapter 11) in APA style.

GitHub's **Cite this repository** button, in the sidebar, generates a citation from the machine-readable
[`CITATION.cff`](CITATION.cff) file in this repository.

**Reusing material.** The book is licensed under [CC BY 4.0](LICENSE). When you share or adapt its
material, give the title, the author, a link to the source, and the license, and say whether you changed
anything, following the Creative Commons
[recommended practices for attribution](https://wiki.creativecommons.org/wiki/Best_practices_for_attribution).

## Building locally

```bash
pip install -r requirements.txt
jupyter-book build .
```

## Author

Devharsh Trivedi, Ph.D., CISSP
