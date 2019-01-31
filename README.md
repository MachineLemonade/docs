# Astronomer Platform Docs

To contribute to our documentation, follow the steps below.

1. Clone the repository on your machine.

`git clone https://github.com/astronomer/docs.git`

2. Head over to our [Website repo](https://github.com/astronomer/website) and clone it on your machine. **Be sure that you have the latest version of the website on your machine before continuing.**

3. Add markdown files for docs and rearrange the `nav.json` file in this repository to adjust the side nav arrangement.

4. From your terminal, run `python3 nav.py`. This will cause that the `docs_nav.json` file in your website directory is up to date with the latest `nav.json` file in your docs directory.

5. Push all docs changes up to Github.

6. Change into your website directory and push all changes up to rebuild preview. Ensure changes look good then merge preview branch into master to rebuild our production site.

## Building Nav Meta

Metadata for navigation is built by `nav.py`. This script parses front matter in the markdown files in the `docs` directory, and the navigation structure defined in `nav.json`.

It depends on Python packages in `requirements.txt`. Run `pip install -r requirements.txt` to install these deps. Then run `python nav.py > ../website/src/layouts/docs_nav.json` to build `docs_nav.json`.
