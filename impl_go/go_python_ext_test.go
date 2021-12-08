package impl_go

import (
	"log"
	"reflect"
	"testing"
	"time"
)

func assertEq(test []string, ans []string) bool {
	return reflect.DeepEqual(test, ans)
}

func Test_process_row(t *testing.T) {

	birthday := "2001-11-19"

	birthday_date, err := time.Parse("2006-01-02", birthday)
	if err != nil {
		log.Fatal("Unable to parse birthday to date: "+birthday, err)
	}

	in_row := in_csv_line{
		full_name:    "Dinorah Navarro",
		birthday:     birthday_date,
		logins:       "24",
		success_rate: 0.913497996499642,
		address:      "914 Washington Run\n15230 New London, Wyoming",
	}
	out_row := process_row(in_row)

	exp_out_row := []string{
		"19-11-2001",
		"DINORAH NAVARRO",
		"H",
		"24",
		"914 Washington Run\n15230 New London, Wyoming",
	}

	if !assertEq(out_row, exp_out_row) {
		t.Logf("Expected %v, got %v", exp_out_row, out_row)
		t.Fail()
	}

}
