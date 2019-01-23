import os
import json
import datetime

import frontmatter

with open('nav.json', 'r') as f:
    nav = json.load(f)

files = {}

for filename in os.listdir('docs'):
    if not filename.endswith('.md'):
        continue

    with open(os.path.join('docs', filename), 'r') as f:
        fm = frontmatter.load(f)
        files[fm['slug']] = fm.metadata

def nav_meta(nav):
    contents = []
    for item in nav:
        if type(item) is str:
            contents.append(files[item])
        else:
            menu = item['menu']
            contents.append({'menu': menu, 'contents': nav_meta(item['contents'])})
    return contents

nav_meta = nav_meta(nav)

def encoder(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

print(json.dumps(nav_meta, indent=2, default=encoder))
