
reqs:
	pip install -U pip-tools
	pip-compile -U --no-emit-trusted-host --no-emit-index-url --build-isolation -o requirements.txt requirements.in


fmt-python:
	isort *.py && black *.py

fmt-rust:
	cd impl_rust && rustfmt **/*.rs

fmt-go:
	gofmt -w impl_go/*.go

fmt: fmt-python fmt-rust fmt-go


build-cython:
	python cython_setup.py build_ext --inplace

build-rust:
	cd impl_rust && cargo rustc --release && ln -fs target/release/librust_python_ext.so rust_python_ext.so

build-go:
	cd impl_go && gopy build -output=out -vm=python3 .

build: build-cython build-rust build-go


test-rust:
	cd impl_rust && cargo test

test-go:
	cd impl_go && go test

test: test-rust test-go


all: fmt test build
