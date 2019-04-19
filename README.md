# Astronomer Docs

This repo contains Markdown files and scripts used to build [Astronomer docs](https://astronomer.io/docs/). We are currently on v0.8 of our docs and all changes should be made in the v`0.8` folder.

## Building docs

1. Run `pip install -r requirements.txt` to install Python dependencies in `requirements.txt`.
1. Clone the [website](https://github.com/astronomer/website) to your machine to a directory next to this one.
1. Run `python scripts/build_nav.py`. This script parses front matter in the markdown files, and the navigation structure defined in `nav.json` to generate `docs_nav.json` in the website project.
1. Push `docs` changes up to Github.
1. Push `website` changes to the `preview` branch, which will trigger a rebuild to the [preview site](https://preview.astronomer.io/docs/).
1. Ensure changes look good, then merge `preview` into `master` to rebuild the production site.
