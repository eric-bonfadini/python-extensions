import filecmp
import os
import timeit
from contextlib import contextmanager

import click
import psutil

from generate_input_data import (
    DEFAULT_INPUT_DELIMITER,
    DEFAULT_INPUT_ENCODING,
    DEFAULT_INPUT_FILEPATH,
    DEFAULT_INPUT_LINE_TERMINATOR,
)
from impl_cython import cython_python_ext
from impl_python import etl_pandas, etl_petl, etl_stdlib

DEFAULT_OUTPUT_DELIMITER = "|"
DEFAULT_OUTPUT_LINE_TERMINATOR = "\n"
DEFAULT_OUTPUT_ENCODING = "utf-8"

FILEPATH_PY3_STDLIB = "/tmp/data/pyt_stdlib.csv"
FILEPATH_PY3_PANDAS = "/tmp/data/pyt_pandas.csv"
FILEPATH_PY3_PETL = "/tmp/data/pyt_petl.csv"
FILEPATH_CYT = "/tmp/data/cyt.csv"


@contextmanager
def perf_logger(label: str):
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss
    start_time = timeit.default_timer()
    yield
    print(f"Elapsed time for [{label}]: {timeit.default_timer() - start_time:.5f}")
    end_mem = process.memory_info().rss
    print(f"Consumed memory for [{label}]: {(end_mem - start_mem) / 1e6:.2f}mb")


@click.command()
@click.option("-i", "--in-filepath", default=DEFAULT_INPUT_FILEPATH)
@click.option("-id", "--in-delimiter", default=DEFAULT_INPUT_DELIMITER)
@click.option("-od", "--out-delimiter", default=DEFAULT_OUTPUT_DELIMITER)
@click.option("-ilt", "--in-line-terminator", default=DEFAULT_INPUT_LINE_TERMINATOR)
@click.option("-olt", "--out-line-terminator", default=DEFAULT_OUTPUT_LINE_TERMINATOR)
@click.option("-ie", "--in-encoding", default=DEFAULT_INPUT_ENCODING)
@click.option("-oe", "--out-encoding", default=DEFAULT_OUTPUT_ENCODING)
def compare(
    in_filepath: str,
    in_delimiter: str,
    out_delimiter: str,
    in_line_terminator: str,
    out_line_terminator: str,
    in_encoding: str,
    out_encoding: str,
):

    with perf_logger("PY3 stdlib"):
        nr_rows = etl_stdlib(
            in_filepath,
            FILEPATH_PY3_STDLIB,
            in_delimiter=in_delimiter,
            out_delimiter=out_delimiter,
            in_line_terminator=in_line_terminator,
            out_line_terminator=out_line_terminator,
            in_encoding=in_encoding,
            out_encoding=out_encoding,
        )
        print(f"{nr_rows} rows processed")

    with perf_logger("PY3 pandas"):
        nr_rows = etl_pandas(
            in_filepath,
            FILEPATH_PY3_PANDAS,
            in_delimiter=in_delimiter,
            out_delimiter=out_delimiter,
            in_line_terminator=in_line_terminator,
            out_line_terminator=out_line_terminator,
            in_encoding=in_encoding,
            out_encoding=out_encoding,
        )
        print(f"{nr_rows} rows processed")
    assert filecmp.cmp(FILEPATH_PY3_STDLIB, FILEPATH_PY3_PANDAS, shallow=False)

    with perf_logger("PY3 petl"):
        nr_rows = etl_petl(
            in_filepath,
            FILEPATH_PY3_PETL,
            in_delimiter=in_delimiter,
            out_delimiter=out_delimiter,
            in_line_terminator=in_line_terminator,
            out_line_terminator=out_line_terminator,
            in_encoding=in_encoding,
            out_encoding=out_encoding,
        )
        print(f"{nr_rows} rows processed")
    assert filecmp.cmp(FILEPATH_PY3_STDLIB, FILEPATH_PY3_PETL, shallow=False)

    with perf_logger("CYT"):
        nr_rows = cython_python_ext.etl(
            in_filepath,
            FILEPATH_CYT,
            in_delimiter=in_delimiter,
            out_delimiter=out_delimiter,
            in_line_terminator=in_line_terminator,
            out_line_terminator=out_line_terminator,
            in_encoding=in_encoding,
            out_encoding=out_encoding,
        )
        print(f"{nr_rows} rows processed")
    assert filecmp.cmp(FILEPATH_PY3_STDLIB, FILEPATH_CYT, shallow=False)


if __name__ == "__main__":
    compare()
