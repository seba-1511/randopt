.PHONY: doc test

all: example

example:
	python examples/simple.py
	roviz.py randopt_result/simple_example

advanced:
	python examples/multi_params.py
	roviz.py multi_params_example

clean:
	rm -rf randopt_results

hb:
	python hb_example.py

evo: 
	python examples/evo_example.py

gs: 
	python examples/gs_example.py

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
	# git tag 0.1 -m "Adds a tag so that we can put this on PyPI."
	# git push --tags origin master
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
