rm dist/*

pydoc-markdown -I src --render-toc > docs\kronoterm_cloud_api_docs.md
git add docs\kronoterm_cloud_api_docs.md
git commit -m "Updated kronoterm_cloud_api_docs.md"

python -m build

python -m twine check dist/*

