import csv

import click
from mimesis import Address, Datetime, Person
from mimesis.random import Random
from tqdm import tqdm

DEFAULT_INPUT_FILEPATH = "/tmp/data/input.csv"
DEFAULT_INPUT_DELIMITER = ","
DEFAULT_INPUT_LINE_TERMINATOR = "\r\n"
DEFAULT_INPUT_ENCODING = "cp1252"


@click.command()
@click.option("-f", "--filepath", default=DEFAULT_INPUT_FILEPATH)
@click.option("-r", "--rows", default=100)
@click.option("-d", "--delimiter", default=DEFAULT_INPUT_DELIMITER)
@click.option("-lt", "--line-terminator", default=DEFAULT_INPUT_LINE_TERMINATOR)
@click.option("-e", "--encoding", default=DEFAULT_INPUT_ENCODING)
def generate_csv(
    filepath: str, rows: int, delimiter: str, line_terminator: str, encoding: str
):

    person = Person("en")
    dt = Datetime()
    rd = Random()
    ad = Address()

    with open(filepath, "w", encoding=encoding) as f_w:
        csv_writer = csv.writer(
            f_w, delimiter=delimiter, lineterminator=line_terminator
        )

        csv_writer.writerow(
            ["full_name", "birthday", "logins", "success_rate", "address"]
        )
        for _ in tqdm(range(rows)):
            new_line = [
                person.full_name(),
                dt.date(),
                rd.randints()[0],
                rd.uniform(0, 1),
                f"{ad.address()}\n{ad.zip_code()} {ad.city()}, {ad.province()}",
            ]
            csv_writer.writerow(new_line)


if __name__ == "__main__":
    generate_csv()
