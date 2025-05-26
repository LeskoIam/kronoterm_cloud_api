rm dist/*

uv sync

pydoc-markdown -I src --render-toc > docs\kronoterm_cloud_api_docs.md

uv build
