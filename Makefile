.PHONY: doc test

all: example

example:
	python examples/simple.py
	roviz.py randopt_results/simple_example/

advanced:
	python examples/multi_params.py
	roviz.py randopt_results/multi_params_example

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

docs:
	rm -rf wiki/docs
	mkdir wiki/docs
	./gendocs.py randopt.samplers > wiki/docs/Samplers-Docs.md
	./gendocs.py randopt.experiment.experiment Experiment > wiki/docs/Experiment-Docs.md
	./gendocs.py randopt.experiment.evolutionary Evolutionary > wiki/docs/Evolutionary-Docs.md
	./gendocs.py randopt.experiment.grid_search GridSearch > wiki/docs/GridSearch-Docs.md
	cd wiki && git add docs/. && git ci -am 'Docs update' && git push
	git ci README.md -m 'README update'

test:
	python -m unittest discover -s 'test' -p '*_tests.py'

publish:
	#http://peterdowns.com/posts/first-time-with-pypi.html
	# TODO: Version bump (2x setup.py) + GH Tag release
	# git tag 0.1 -m "Adds a tag so that we can put this on PyPI."
	# git push --tags origin master
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
