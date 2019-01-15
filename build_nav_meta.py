import os
import json

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

out = []
for item in nav:
    if type(item) is str:
        out.append(files[item])

print(out)
