package impl_go

import (
	"encoding/csv"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"golang.org/x/text/encoding/charmap"
)

type in_csv_line struct {
	full_name    string
	birthday     time.Time
	logins       string
	success_rate float32
	address      string
}

func get_reader(encoding string, file *os.File) *csv.Reader {
	if encoding == "utf-8" {
		return csv.NewReader(file)
	} else if encoding == "latin-1" {
		return csv.NewReader(charmap.ISO8859_1.NewDecoder().Reader(file))
	} else if encoding == "cp1252" {
		return csv.NewReader(charmap.Windows1252.NewDecoder().Reader(file))
	} else {
		log.Fatal("Unknown encoding " + encoding)
		return nil
	}
}

func get_writer(encoding string, file *os.File) *csv.Writer {
	if encoding == "utf-8" {
		return csv.NewWriter(file)
	} else if encoding == "latin-1" {
		return csv.NewWriter(charmap.ISO8859_1.NewEncoder().Writer(file))
	} else if encoding == "cp1252" {
		return csv.NewWriter(charmap.Windows1252.NewEncoder().Writer(file))
	} else {
		log.Fatal("Unknown encoding " + encoding)
		return nil
	}
}

func process_row(in_row in_csv_line) []string {

	success_rate_str := "H"
	if in_row.success_rate < 0.5 {
		success_rate_str = "L"
	}

	return []string{
		in_row.birthday.Format("02-01-2006"),
		strings.ToUpper(in_row.full_name),
		success_rate_str,
		in_row.logins,
		in_row.address,
	}
	// fmt.Println(out_line)
}

// Etl perform etl on an input csv
func Etl(in_filepath, out_filepath, in_delimiter, out_delimiter, in_line_terminator, out_line_terminator, in_encoding, out_encoding string) int {

	in_f, err := os.Open(in_filepath)
	if err != nil {
		log.Fatal("Unable to open input file "+in_filepath, err)
	}
	defer in_f.Close()

	out_f, err := os.Create(out_filepath)
	if err != nil {
		log.Fatal("Unable to open output file "+out_filepath, err)
	}
	defer out_f.Close()

	nr_rows := 0

	csvReader := get_reader(in_encoding, in_f)
	csvReader.Comma = []rune(in_delimiter)[0]
	csvReader.LazyQuotes = true

	csvWriter := get_writer(out_encoding, out_f)
	csvWriter.Comma = []rune(out_delimiter)[0]
	if out_line_terminator == "\r\n" {
		csvWriter.UseCRLF = true
	}

	defer csvWriter.Flush()

	out_header_line := []string{
		"birthday", "full_name", "success_rate", "logins", "address",
	}

	if err := csvWriter.Write(out_header_line); err != nil {
		log.Fatalln("error writing header to output file", err)
	}

	if _, err := csvReader.Read(); err != nil {
		log.Fatalln("Unable to read header from csv", err)
	}

	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal("Unable to parse file as CSV for "+in_filepath, err)
		}
		success_rate, err := strconv.ParseFloat(record[3], 32)
		if err != nil {
			log.Fatal("Unable to parse logins to float32: "+record[3], err)
		}
		birthday_date, err := time.Parse("2006-01-02", record[1])
		if err != nil {
			log.Fatal("Unable to parse birthday to date: "+record[1], err)
		}
		in_row := in_csv_line{
			full_name:    record[0],
			birthday:     birthday_date,
			logins:       record[2],
			success_rate: float32(success_rate),
			address:      record[4],
		}
		out_line := process_row(in_row)

		if err := csvWriter.Write(out_line); err != nil {
			log.Fatalln("error writing record to file", err)
		}

		nr_rows += 1
	}

	return nr_rows
}
