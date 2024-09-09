rm dist/*

pydoc-markdown -I src --render-toc > docs\kronoterm_cloud_api_docs.md

python -m pip install -U -r requirements.txt

python -m build

python -m twine check dist/*

