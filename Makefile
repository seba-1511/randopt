.PHONY: docs test

all: 
	rm -rf randopt_results
	python examples/command.py test1 --arg1 21 --arg2 name2 --arg3=4.56
	python examples/command.py test2 --arg1 21 --arg2 name2
	python examples/command.py --help
	python examples/command.py --help test2
	python examples/command.py test_experiment1 --x 3 --y 4
	python examples/command.py test_experiment2 --x 1 --y 3
	python examples/command.py test_experiment3 --x 1 --y 3

dev:
	python setup.py develop

clean:
	rm -rf randopt_results

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
	make clean
	python -m unittest discover -s 'test' -p '*_tests.py'
	python examples/simple.py
	python examples/multi_params.py
	python examples/evo_example.py
	python examples/gs_example.py
	python examples/grad_descent.py
	python examples/attachments_example.py
	python examples/objective_examples.py
	python examples/summary_list_example.py
	python examples/command.py test1 --arg1 21 --arg2 name2 --arg3=4.56
	python examples/command.py test2 --arg1 21 --arg2 name2
	python examples/command.py --help
	python examples/command.py --help test2
	python examples/command.py test_experiment1 --x 3 --y 4
	python examples/command.py test_experiment2 --x 1 --y 3
	python examples/command.py test_experiment3 --x 1 --y 3

publish:
	#http://peterdowns.com/posts/first-time-with-pypi.html
	# TODO: Version bump (2x setup.py) + GH Tag release
	# git tag 0.1 -m "Adds a tag so that we can put this on PyPI."
	# git push --tags origin master
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
