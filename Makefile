

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
