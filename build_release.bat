rm dist/*

python -m bumpver update --patch

python -m build

python -m twine check dist/*
python -m twine upload dist/*
