import parsecsv, os, streams, strutils, nimpy, times, encodings


proc quote_if_needed(st: string, separator: string): string =
  var out_str = st
  if separator in st or "\n" in st or "\r" in st or "\r\n" in st:
    out_str = "\"" & st & "\""
  return out_str

proc build_csv_row(output_row: array[0..4, string], delimiter: string,
    line_terminator: string, out_encoding: string,
        in_encoding: string): string =
  let quoted_row = [output_row[0], quote_if_needed(output_row[1], delimiter),
      output_row[2], output_row[3], quote_if_needed(output_row[4], delimiter)]
  return convert(quoted_row.join(delimiter) & line_terminator,
        out_encoding, in_encoding)

proc process_row*(row: array[0..4, string],
    separator: string): array[0..4, string] =
  return [
    parse(row[0], "yyyy-MM-dd").format("dd-MM-yyyy"),
    toUpperAscii(row[1]),
    if parseFloat(row[2]) > 0.5: "H" else: "L",
    row[3],
    row[4]
    ]

proc etl(in_filepath: string, out_filepath: string,
    in_delimiter: string, out_delimiter: string,
        in_line_terminator: string, out_line_terminator: string,
        in_encoding: string, out_encoding: string): int {.exportpy.} =

  let in_file = newFileStream(in_filepath, fmRead)
  if in_file == nil:
    quit("cannot open the file " & in_filepath)
  defer: in_file.close()

  let out_file = newFileStream(out_filepath, fmWrite)
  if out_file == nil:
    quit("cannot open the file " & out_filepath)
  defer: out_file.close()

  var csv: CsvParser
  open(csv, in_file, in_filepath, separator = in_delimiter[0])

  csv.readHeaderRow()
  out_file.write(build_csv_row(["birthday", "full_name", "success_rate",
      "logins", "address"], out_delimiter, out_line_terminator, out_encoding, in_encoding))

  var nr_rows = 0
  while csv.readRow():
    let input_row = [csv.rowEntry("birthday"), csv.rowEntry("full_name"),
        csv.rowEntry("success_rate"), csv.rowEntry("logins"), csv.rowEntry("address")]
    var output_row = process_row(input_row, out_delimiter)
    out_file.write(build_csv_row(output_row, out_delimiter, out_line_terminator,
        out_encoding, in_encoding))
    inc nr_rows

  return nr_rows
