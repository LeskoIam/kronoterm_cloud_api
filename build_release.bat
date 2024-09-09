rm dist/*

python -m bumpver update --%1

python -m build

python -m twine check dist/*
python -m twine upload dist/*
