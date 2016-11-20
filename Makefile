

all: hb

example:
	python example.py

complex:
	python complexTest.py

hb:
	python hb_example.py

viz:
	roviz.py -e myexp

dev:
	python setup.py develop
