
reqs:
	pip install pip-tools
	pip-compile -U --no-emit-trusted-host --no-emit-index-url --build-isolation -o requirements.txt requirements.in


fmt-python:
	isort *.py && black *.py

fmt: fmt-python

build-cython:
	python cython_setup.py build_ext --inplace

build: build-cython


all: fmt build
