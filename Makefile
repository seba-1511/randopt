.PHONY: doc
	
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

doc:
	rm -rf doc
	mkdir -p doc
	pydoc -w randopt
	pydoc -w randopt.experiment
	pydoc -w randopt.samplers
	mv *.html doc
