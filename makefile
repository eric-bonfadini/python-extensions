
reqs:
	pip install -U pip-tools
	pip-compile -U --no-emit-trusted-host --no-emit-index-url --build-isolation -o requirements.txt requirements.in


fmt-python:
	isort *.py && black *.py

fmt-rust:
	cd impl_rust && rustfmt **/*.rs

fmt-go:
	gofmt -w impl_go/*.go

fmt-nim:
	cd impl_nim && nimpretty **/*.nim

fmt: fmt-python fmt-rust fmt-go fmt-nim


build-cython:
	python cython_setup.py build_ext --inplace

build-rust:
	cd impl_rust && cargo rustc --release && ln -fs target/release/librust_python_ext.so rust_python_ext.so

build-go:
	cd impl_go && gopy build -output=out -vm=python3 .

build-nim:
	cd impl_nim && nim c -d:release --threads:on --app:lib --out:nim_python_ext.so src/nim_python_ext.nim

build: build-cython build-rust build-go build-nim


test-rust:
	cd impl_rust && cargo test

test-go:
	cd impl_go && go test

test-nim:
    # not working because of https://github.com/nim-lang/Nim/pull/19018
	cd impl_nim && testament p tests/*.nim

test: test-rust test-go # test-nim


all: fmt test build
