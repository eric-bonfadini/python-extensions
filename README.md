# python-extensions

In this project I'm creating python extensions using different programming languages.
Instead of hello-world examples, I'm gonna try a simple ETL use case: each version will import the extension in python, read an input CSV with a few columns (and specific encoding/separator/terminator), perform some transformations and write an output CSV (with different encoding/separator/terminator).

For each implementation I will use the standard library of the programming language or specific frameworks if available, and I will write a paragraph with details.

Python's requirements are pinned using [pip-tools](https://github.com/jazzband/pip-tools).
The Dockerfile can be used in a devcontainer in order to have an environment with everything properly configured.

## Input file

The script [generate_input_data.py](generate_input_data.py) is used in order to create the input CSV with random data, using mimesis.
The input CSV is made up of 5 columns: a full name, a birthday, a number of logins, a success rate and an address (quoted):

| full_name    | birthday   | logins | success_rate      | address                                                   |
| ------------ | ---------- | ------ | ----------------- | --------------------------------------------------------- |
| Sandee Blair | 2013-12-24 | 33     | 0.709501198353512 | "1073 Turk Murphy Promenade\n73927 Carson City, Missouri" |
