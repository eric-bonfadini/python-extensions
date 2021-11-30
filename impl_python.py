import csv
from datetime import datetime

import numpy as np
import pandas as pd
import petl as etl

DATE_FROM_FORMAT = "%Y-%m-%d"
DATE_TO_FORMAT = "%d-%m-%Y"

FLAG_SUCCESS_HIGH = "H"
FLAG_SUCCESS_LOW = "L"

SUCCESS_RATE_THRESHOLD = 0.5


def etl_stdlib(
    in_filepath: str,
    out_filepath: str,
    in_delimiter: str,
    out_delimiter: str,
    in_line_terminator: str,
    out_line_terminator: str,
    in_encoding: str,
    out_encoding: str,
) -> int:

    nr_rows = 0

    with open(in_filepath, "r", encoding=in_encoding) as f_r, open(
        out_filepath, "w", encoding=out_encoding
    ) as f_w:
        csv_reader = csv.reader(
            f_r, delimiter=in_delimiter, lineterminator=in_line_terminator
        )
        csv_writer = csv.writer(
            f_w, delimiter=out_delimiter, lineterminator=out_line_terminator
        )

        next(csv_reader)
        csv_writer.writerow(
            ["birthday", "full_name", "success_rate", "logins", "address"]
        )
        for line in csv_reader:
            new_line = [
                datetime.strptime(line[1], DATE_FROM_FORMAT).strftime(DATE_TO_FORMAT),
                line[0].upper(),
                FLAG_SUCCESS_HIGH
                if float(line[3]) > SUCCESS_RATE_THRESHOLD
                else FLAG_SUCCESS_LOW,
                line[2],
                line[4],
            ]
            csv_writer.writerow(new_line)
            nr_rows += 1

        return nr_rows


def etl_pandas(
    in_filepath: str,
    out_filepath: str,
    in_delimiter: str,
    out_delimiter: str,
    in_line_terminator: str,
    out_line_terminator: str,
    in_encoding: str,
    out_encoding: str,
) -> int:
    df = pd.read_csv(
        in_filepath,
        sep=in_delimiter,
        header=0,
        encoding=in_encoding,
        converters={"success_rate": np.float32, "logins": np.int8},
        parse_dates=["birthday"],
    )

    df["success_rate"] = np.where(
        df["success_rate"] > SUCCESS_RATE_THRESHOLD, FLAG_SUCCESS_HIGH, FLAG_SUCCESS_LOW
    )
    df["success_rate"] = df["success_rate"].astype("category")

    df["full_name"] = df["full_name"].str.upper()

    df[["birthday", "full_name", "success_rate", "logins", "address"]].to_csv(
        out_filepath,
        header=True,
        sep=out_delimiter,
        index=False,
        encoding=out_encoding,
        line_terminator=out_line_terminator,
        date_format=DATE_TO_FORMAT,
    )

    return len(df)


def etl_petl(
    in_filepath: str,
    out_filepath: str,
    in_delimiter: str,
    out_delimiter: str,
    in_line_terminator: str,
    out_line_terminator: str,
    in_encoding: str,
    out_encoding: str,
) -> int:
    table = etl.fromcsv(
        in_filepath,
        delimiter=in_delimiter,
        lineterminator=in_line_terminator,
        encoding=in_encoding,
    )
    table = (
        etl.movefield(table, "birthday", 0)
        .movefield("success_rate", 2)
        .convert("full_name", lambda v: v.upper())
        .convert(
            "success_rate",
            lambda v: FLAG_SUCCESS_HIGH
            if float(v) > SUCCESS_RATE_THRESHOLD
            else FLAG_SUCCESS_LOW,
        )
        .convert(
            "birthday",
            lambda x: datetime.strptime(x, DATE_FROM_FORMAT).strftime(DATE_TO_FORMAT),
        )
    )
    table.tocsv(
        out_filepath,
        delimiter=out_delimiter,
        lineterminator=out_line_terminator,
        encoding=out_encoding,
    )
    return len(table) - 1
