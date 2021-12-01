cimport cython
import csv

from cpython.datetime cimport datetime

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef int etl(
    in_filepath: str, 
    out_filepath: str, 
    in_delimiter: str, 
    out_delimiter: str, 
    in_line_terminator: str, 
    out_line_terminator: str, 
    in_encoding: str,
    out_encoding: str
):

    cdef long nr_rows = 0

    with open(in_filepath, "r", encoding=in_encoding) as f_r, open(
        out_filepath, "w", encoding=out_encoding
    ) as f_w:
        csv_reader = csv.reader(f_r, delimiter=in_delimiter, lineterminator=in_line_terminator)
        csv_writer = csv.writer(f_w, delimiter=out_delimiter, lineterminator=out_line_terminator)
        
        next(csv_reader)
        csv_writer.writerow(["birthday", "full_name", "success_rate", "logins", "address"])
        for full_name, birthday, logins, success_rate, address in csv_reader:
            new_line = [
                datetime.strptime(birthday, "%Y-%m-%d").strftime("%d-%m-%Y"),
                full_name.upper(),
                "H" if float(success_rate) > 0.5 else "L",
                logins,
                address,
            ]
            csv_writer.writerow(new_line)
            nr_rows += 1

        return nr_rows
