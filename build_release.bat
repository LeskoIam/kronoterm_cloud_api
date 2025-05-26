rm dist/*

uv sync

pydoc-markdown -I kronoterm_cloud_api --render-toc > docs\kronoterm_cloud_api_docs.md
git add docs\kronoterm_cloud_api_docs.md
git commit docs\kronoterm_cloud_api_docs.md -m "Updated KronotermCloudApi documentation."

python -m bumpver update --%1

uv build
