rm dist/*

python -m build

python -m twine check dist/*

