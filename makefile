
reqs:
	pip install pip-tools
	pip-compile -U --no-emit-trusted-host --no-emit-index-url --build-isolation -o requirements.txt requirements.in


fmt-python:
	isort *.py && black *.py

fmt-rust:
	cd impl_rust && rustfmt **/*.rs

fmt: fmt-python fmt-rust


build-cython:
	python cython_setup.py build_ext --inplace

build-rust:
	cd impl_rust && cargo rustc --release && ln -fs target/release/librust_python_ext.so rust_python_ext.so

build: build-cython build-rust


test-rust:
	cd impl_rust && cargo test

test: test-rust


all: fmt test build
