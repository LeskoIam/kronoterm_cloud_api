rm dist/*

pydoc-markdown -I kronoterm_cloud_api --render-toc > docs\kronoterm_cloud_api_docs.md
git add docs\kronoterm_cloud_api_docs.md
git commit docs\kronoterm_cloud_api_docs.md -m "Updated kronoterm_cloud_api_docs.md"

python -m pip install -r requirements.txt

python -m bumpver update --%1

python -m build

python -m twine check dist/*
python -m twine upload dist/*
