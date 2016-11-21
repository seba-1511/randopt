.PHONY: doc test

all: example

example:
	python examples/simple.py
	roviz.py -e simple_example

advanced:
	python examples/multi_params.py
	roviz.py -e multi_params_example

clean:
	rm -rf randopt_results

hb:
	python hb_example.py

dev:
	python setup.py develop

doc:
	rm -rf doc
	mkdir -p doc
	pydoc -w randopt
	pydoc -w randopt.experiment
	pydoc -w randopt.samplers
	mv *.html doc

test:
	python -m unittest discover -s 'test' -p '*_tests.py'

web: doc
	cp ./doc/* ./web/

publish:
	#http://peterdowns.com/posts/first-time-with-pypi.html
	# TODO: Version bump (2x setup.py) + GH Tag release
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
