# Astronomer Platform Docs

## Building Nav Meta


1. Create yourself a virtualenv and activate it i.e.
```
python3 -m venv venv
. venv/bin/activate
```
2. Install requirements within your venv

`pip install -r requirements.txt`

3. Use [invoke](http://www.pyinvoke.org/) (Make on steroids written in Python) to invoke the `render` task in [tasks.py](tasks.py)

`inv render`

This task parses front matter in the markdown files in the `docs` directory, and the navigation structure defined in `nav.json`.
