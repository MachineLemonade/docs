# Astronomer Docs

This repo contains Markdown files and scripts used to build [Astronomer docs](https://astronomer.io/docs/). We are currently on v0.8 of our docs and all changes should be made in the v`0.8` folder.

## Writing Docs

Each of the docs on our site are built from the markdown files in this repository. Our website uses the npm package [processmd](https://www.npmjs.com/package/processmd) to convert all of the markdown to JSON blobs on build. It then has some custom React components that take care of applying some custom styles to the JSON blobs and rendering them in the browser.

**There are a few structural guidelines that must be followed when contributing to this repository**:
1. Do not use H1s (applied in markdown as a single `#`) in the body your files. The frontmatter `Title` field is what is translated into the page H1 by our website code, so having extra H1s results in bad styling and redundancy.
2. Delineate between major sections of docs with *clear and concise* H2s (applied in markdown as a double `##`). The Content Navigator, which allows you to easily navigate and link to specific sections of a given doc, is generated from only H2s. Since this navigator allows you to link to these H2s, they must not be overly verbose, as this will result in a poor UX.



## Building Docs

1. Run `pip install -r requirements.txt` to install Python dependencies in `requirements.txt`.
1. Clone the [website](https://github.com/astronomer/website) to your machine to a directory next to this one.
1. Run `python scripts/build_nav.py`. This script parses front matter in the markdown files, and the navigation structure defined in `nav.json` to generate `docs_nav.json` in the website project.
1. Push `docs` changes up to Github.
1. Push `website` changes to the `preview` branch, which will trigger a rebuild to the [preview site](https://preview.astronomer.io/docs/).
1. Ensure changes look good, then merge `preview` into `master` to rebuild the production site.
