rm dist/*

python -m pip install -r requirements.txt

pydoc-markdown -I src --render-toc > docs\kronoterm_cloud_api_docs.md

uv build
