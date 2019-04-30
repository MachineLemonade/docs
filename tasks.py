from pprint import pprint
from pathlib import Path
import datetime as dt
import atexit
import json
import os

from invoke import task

import frontmatter


@task
def render(c):
    """
    Render the docs and run the site on localhost:3000.

    Hacky implementation for now -- will improve later.

    This task parses front matter in the markdown files in the `docs` directory, 
    and the navigation structure defined in `nav.json`.
    
    """
    print('writing the following to the docs_nav.json file...')

    new_layouts_content = get_metadata()

    print(new_layouts_content)

    with c.cd("../website"):
        with c.cd("src/layouts/"):
            nav_file = Path(Path.cwd(), "docs_nav.json")
            original_layouts_content = nav_file.read_text()

            # ensure the original docs_nav goes back to normal
            atexit.register(nav_file.write_text, original_layouts_content)

            nav_file.write_text(new_layouts_content)
        # TODO: fetch content from local filesystem
        c.run("npm run local")


def get_metadata():
    """Returns nav data as a json string."""
    nav = json.loads(Path("nav.json").read_text())

    files = {}

    for file_ in Path("docs").glob("*.md"):
        fm = frontmatter.loads(file_.read_text())
        files[fm["slug"]] = fm.metadata

    def transform_metadata(nav=nav):
        contents = []
        for item in nav:
            if type(item) is str:
                contents.append(files[item])
            else:
                contents.append(
                    {
                        "menu": item["menu"],
                        "contents": transform_metadata(item["contents"]),
                    }
                )
        return contents

    def encoder(o):
        if isinstance(o, (dt.date, dt.datetime)):
            return o.isoformat()

    return json.dumps(transform_metadata(), indent=2, default=encoder)
