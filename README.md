# Astronomer Docs

This repo contains Markdown files and scripts used to build [Astronomer docs](https://astronomer.io/docs/). We are currently on v0.11 of our docs and all changes should be made in the v`0.11` folder.

## Writing Docs

Each of the docs on our site are built from the markdown files in this repository. Our website uses the npm package [processmd](https://www.npmjs.com/package/processmd) to convert all of the markdown to JSON blobs on build. It then has some custom React components that take care of applying some custom styles to the JSON blobs and rendering them in the browser.

**There are a few structural guidelines that must be followed when contributing to this repository**:
1. Do not use H1s (applied in markdown as a single `#`) in the body your files. The frontmatter `Title` field is what is translated into the page H1 by our website code, so having extra H1s results in bad styling and redundancy.
2. Delineate between major sections of docs with *clear and concise* H2s (applied in markdown as a double `##`). The Content Navigator, which allows you to easily navigate and link to specific sections of a given doc, is generated from only H2s. Since this navigator allows you to link to these H2s, they must not be overly verbose, as this will result in a poor UX.

## Changing Nav Structure

When you'd like to add to, remove from, or change the docs navigation menu, you can do so in the `nav_structure.json` files located in the `nav` folder of each versioned directory. Be sure that all slugs that you add match both the frontmatter slug you've added to the doc and the file name. Once `nav_structure.json` has been changed to your liking, run `python scripts/build_nav.py` to auto-build the official `docs_nav.json` files with all of the frontmatter from the docs.

> While it may seem redundant to have two nav files, we've decided it's a better UX to have one file focused purely on nav structure and another with all of the official "production" information that our website uses to build the webpages and add SEO tags. This way, you need to deal with less JSON formatting and don't need to replicate the frontmatter in two separate places.


## Building Docs

1. Run `pip install -r requirements.txt` to install Python dependencies in `requirements.txt`.
2. Run `python scripts/build_nav.py`. This script parses front matter in the markdown files, and the navigation structure defined in `nav_structure.json` to generate `docs_nav.json` in the same folder project. *Do not* edit the docs_nav.json files directly- these should all be auto-generated from the `build_nav.py` script.
3. Push `docs` changes up to Github. This will trigger a rebuild of preview.astronomer.io. Contact a website admin (pete@astronomer.io) for the password.
4. View your doc on preview.astronomer.io and confirm it reads and formats as expected.
5. Rebuild production website in Netlify when the doc is ready to be publicized.
