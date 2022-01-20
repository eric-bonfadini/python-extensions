import ../src/nim_python_ext

let input_row = ["2001-11-19", "Dinorah Navarro", "0.913497996499642", "24",
    "914 Washington Run\n15230 New London, Wyoming"]
let res = process_row(input_row, "\"")
echo res
assert res == ["19-11-2001", "DINORAH NAVARRO", "H", "24", "914 Washington Run\n15230 New London, Wyoming"]
