setup:
	rm -rf dist; python setup.py bdist_wheel

install:
	pip install "dist/"$(shell ls dist)

upload:
	twine upload "dist/"$(shell ls dist)

all: setup install upload
