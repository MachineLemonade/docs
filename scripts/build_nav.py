import os
import json
import datetime
import frontmatter

versions = []
for filename in os.listdir("."):
    if filename.startswith('v'):
        versions.append(filename)


for version in versions:
    with open(version + '/nav/nav_structure.json', 'r') as f:
        nav = json.load(f)

    files = {}

    for filename in os.listdir(version):
        if not filename.endswith('.md'):
            continue

        with open(os.path.join(version, filename), 'r') as f:
            fm = frontmatter.load(f)

            files[fm['slug']] = fm.metadata

    def nav_meta(nav):
        contents = []
        for item in nav:
            if type(item) is dict:
                menu = item['menu']
                contents.append({'menu': menu, 'contents': nav_meta(item['contents'])})
            else:
                contents.append(files[item])
        return contents

    nav_meta = nav_meta(nav)

    def encoder(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    path = "./" + version + "/nav/docs_nav.json"
    print("Creating... " + path)
    f = open(path, "w")
    f.write(json.dumps(nav_meta, indent=2, default=encoder))
    f.close()
