# python-extensions

In this project I'm creating python extensions using different programming languages.
Instead of hello-world examples, I'm gonna try a simple ETL use case: each version will import the extension in python, read an input CSV with a few columns (and specific encoding/separator/terminator), perform some transformations and write an output CSV (with different encoding/separator/terminator).

For each implementation I will use the standard library of the programming language or specific frameworks if available, and I will write a paragraph with details.

Python's requirements are pinned using [pip-tools](https://github.com/jazzband/pip-tools).
The Dockerfile can be used in a devcontainer in order to have an environment with everything properly configured.

## Generate input

The script [generate_input_data.py](generate_input_data.py) is used in order to create the input CSV with random data, using mimesis.
The input CSV is made up of 5 columns: a full name, a birthday, a number of logins, a success rate and an address (quoted):

| full_name    | birthday   | logins | success_rate      | address                                                   |
| ------------ | ---------- | ------ | ----------------- | --------------------------------------------------------- |
| Sandee Blair | 2013-12-24 | 33     | 0.709501198353512 | "1073 Turk Murphy Promenade\n73927 Carson City, Missouri" |

## Compare

The script [compare.py](compare.py) allows to generate output files (printing also time/memory taken) and to compare each file to the master output (python standard lib version).
Each implementation gets 8 params in input (in/out filepath, in/out delimiter, in/out line_terminator, in/out encoding) and returns the number of rows processed.

**Note: this is not a benchmark between all the implementations, but it's just a way to show how to integrate different languages in python using a "real" use case. Each implementation can probably be much more elegant/idiomatic/fast/efficient.**

## Implementations

### Python native

The script [impl_python.py](impl_python.py) contains implementations in native python code, using:
- python standard lib
- pandas
- petl

### Cython

The folder impl_cython contains the cython implementation ([cython_python_ext.pyx](impl_cython/cython_python_ext.pyx)).
Cython is installed as a python lib, defined inside requirements.in/txt

This extension can be built with `make build-cython`. Once built, the impl_cython folder will contain:
- the .cpp version of the code
- an .html file with annotations
- the .so file that will be imported in python

### Rust

Rust (version 1.57.0) is installed in the Dockerfile; the integration with python is possible using the Rust library PyO3.
The folder impl_rust contains the rust implementation ([lib.rs](impl_rust/src/lib.rs)) and the configuration ([Cargo.toml](impl_rust/Cargo.toml)).
Tests are inside the same file and can be run with `make test-rust`.

This extension can be built with `make build-rust`. Once built, the extension will be in the target folder (with a symbolic link that will be imported in python).

### Go

Go (version 1.17.4) is installed in the Dockerfile; the integration with python is possible using the go library gopy + the python library pybindgen.
The folder impl_go contains the go implementation ([go_python_ext.go](impl_go/go_python_ext.go)) and the configuration ([go.mod](impl_go/go.mod)).
Tests are in ([go_python_ext_test.go](impl_go/go_python_ext_tets.go))  and can be run with `make test-go`.

This extension can be built with `make build-go`. Once built, the extension will be in the out folder.
