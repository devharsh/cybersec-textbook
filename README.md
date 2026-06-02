# Cybersecurity: Theory, Practice, and Ethics

A free, open-source textbook for university courses and professional certifications, by
Devharsh Trivedi, Ph.D., CISSP (Bowie State University).

## Build locally

```bash
pip install jupyter-book
jupyter-book build .
```

The rendered site appears in `_build/html/index.html`.

## Publish on GitHub Pages

```bash
pip install ghp-import
ghp-import -n -p -f _build/html
```

## Structure

- `intro.md` landing page
- `_toc.yml` table of contents
- `_config.yml` build configuration
- `references.bib` bibliography
- `chapters/` 17 chapters, a preface, and three appendices as Jupyter notebooks

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).
