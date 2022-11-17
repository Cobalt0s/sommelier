setup: clean
	python3 setup.py bdist_wheel

install:
	pip install "dist/"$(shell ls dist)

upload:
	twine upload "dist/"$(shell ls dist)

clean:
	rm -rf dist; rm -rf build

all: setup install upload
	rm -rf dist; rm -rf build
