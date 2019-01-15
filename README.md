# Astronomer Platform Docs

## Building Nav Meta
Metadata for navigation is built by `build_nav_meta.py`. This script parses front matter in the markdown files in the `docs` directory, and the navigation structure defined in `nav.json`.

It depends on Python packages in `requirements.txt`. Run `pip install -r requirements.txt` to install these deps. Then run `python build_nav_meta.py` to build `nav_meta.json`.
