

all: viz

example:
	python example.py

complex:
	python complexTest.py

viz:
	roviz.py -e myexp

dev:
	python setup.py develop
