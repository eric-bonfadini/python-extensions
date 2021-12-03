extern crate chrono;
extern crate csv;
extern crate serde;
#[macro_use]
extern crate serde_derive;

use std::error::Error;

use std::fs::File;

use encoding_rs::Encoding;
use encoding_rs_io::DecodeReaderBytesBuilder;

use chrono::NaiveDate;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[derive(Debug, Deserialize)]
#[serde()]
struct RecordIn {
    full_name: String,
    birthday: String,
    logins: String,
    success_rate: f32,
    address: String,
}

#[derive(Debug, Serialize, PartialEq)]
#[serde()]
struct RecordOut {
    birthday: String,
    full_name: String,
    success_rate: String,
    logins: String,
    address: String,
}

fn process_row(rec_in: RecordIn) -> Result<RecordOut, Box<dyn Error>> {
    let value = if rec_in.success_rate > 0.5 {
        "H".to_string()
    } else {
        "L".to_string()
    };
    let date_only = NaiveDate::parse_from_str(&rec_in.birthday, "%Y-%m-%d")?;
    return Ok(RecordOut {
        birthday: date_only.format("%d-%m-%Y").to_string(),
        full_name: rec_in.full_name.to_uppercase(),
        success_rate: value,
        logins: rec_in.logins,
        address: rec_in.address,
    });
}

fn run(
    in_filepath: String,
    out_filepath: String,
    in_delimiter: String,
    out_delimiter: String,
    _in_line_terminator: String,
    out_line_terminator: String,
    in_encoding: String,
    _out_encoding: String,
) -> Result<i32, Box<dyn Error>> {
    let file = File::open(in_filepath)?;
    let transcoded = DecodeReaderBytesBuilder::new()
        .encoding(Encoding::for_label(in_encoding.as_bytes()))
        .build(file);
    let mut rdr = csv::ReaderBuilder::new()
        .delimiter(in_delimiter.as_bytes()[0])
        //.terminator(csv::Terminator::Any(in_line_terminator.as_bytes()[0]))
        .from_reader(transcoded);

    let mut t = csv::Terminator::Any(out_line_terminator.as_bytes()[0]);
    if out_line_terminator == "\r\n" {
        t = csv::Terminator::CRLF;
    }

    let mut wtr = csv::WriterBuilder::new()
        .delimiter(out_delimiter.as_bytes()[0])
        .terminator(t)
        .from_path(out_filepath)?;

    let mut nr_rows = 0;
    for result in rdr.deserialize() {
        let rec_in: RecordIn = result?;
        let rec_out = process_row(rec_in)?;
        wtr.serialize(rec_out)?;
        nr_rows += 1
    }
    wtr.flush()?;
    Ok(nr_rows)
}

#[pyfunction]
fn etl(
    in_filepath: String,
    out_filepath: String,
    in_delimiter: String,
    out_delimiter: String,
    in_line_terminator: String,
    out_line_terminator: String,
    in_encoding: String,
    out_encoding: String,
) -> PyResult<i32> {
    let nr_rows = run(
        in_filepath,
        out_filepath,
        in_delimiter,
        out_delimiter,
        in_line_terminator,
        out_line_terminator,
        in_encoding,
        out_encoding,
    )
    .expect("Can't run etl");
    Ok(nr_rows)
}

#[pymodule]
fn rust_python_ext(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(etl))?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_row() -> Result<(), Box<dyn Error>> {
        let rec_in = RecordIn {
            full_name: "Dinorah Navarro".to_string(),
            birthday: "2001-11-19".to_string(),
            logins: "24".to_string(),
            success_rate: 0.913497996499642,
            address: "914 Washington Run\n15230 New London, Wyoming".to_string(),
        };
        let exp = RecordOut {
            birthday: "19-11-2001".to_string(),
            full_name: "DINORAH NAVARRO".to_string(),
            success_rate: "H".to_string(),
            logins: "24".to_string(),
            address: "914 Washington Run\n15230 New London, Wyoming".to_string(),
        };
        assert_eq!(process_row(rec_in)?, exp);
        Ok(())
    }
}
