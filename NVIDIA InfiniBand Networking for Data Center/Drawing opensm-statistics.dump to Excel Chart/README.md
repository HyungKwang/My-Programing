# OpenSM Statistics Dump to Excel Charts

## Intro

This script reads an `opensm-statistics.dump` CSV file from OpenSM and creates an Excel workbook with raw statistics, normal charts, and delta charts.

It is useful when you want to quickly visualize OpenSM counter changes over time without manually building Excel charts for every column.

The script creates charts based on `TIME_STAMP` and every numeric statistics column.

## Main Features

- Reads `opensm-statistics.dump` CSV data.
- Keeps `TIME_STAMP` displayed in Excel like the original dump format.

```text
Mar 28 09:22:14
```

- Creates an Excel workbook with 3 sheets:

```text
OpenSM_Statistics   - filtered raw data
Charts              - normal line charts for each numeric column
Delta Charts        - delta line charts for each numeric column
```

- Supports optional time range filtering.

```cmd
-t "Mar 28 09:22:14 ~ Apr 11 17:20:36"
```

- Supports limiting chart count for quick testing.

```cmd
--max-charts 10
```

## Delta Chart Meaning

The `Delta Charts` sheet calculates the difference between the current row and the previous row for each numeric column.

Example with `LIGHT_SWEEP_COUNT`:

```text
Raw data:
3747077
3747438
3747799

Delta data:
3747438 - 3747077 = 361
3747799 - 3747438 = 361
```

The delta data is then used to draw charts by `TIME_STAMP`.

## Running Environment

This script was created and tested on Windows CMD.

Tested environment:

```cmd
python --version
Python 3.13.3
```

Required Python library:

```cmd
pip install openpyxl
```

## Files

```text
dump_to_excel_charts.py          Main Python script
opensm-statistics.dump           Input OpenSM statistics dump file
opensm-statistics_charts.xlsx    Example output Excel workbook
```

## How to Run

Open Windows CMD in the folder that contains `dump_to_excel_charts.py` and `opensm-statistics.dump`.

Default run:

```cmd
python dump_to_excel_charts.py
```

Specify input dump file:

```cmd
python dump_to_excel_charts.py opensm-statistics.dump
```

Specify output Excel file:

```cmd
python dump_to_excel_charts.py opensm-statistics.dump -o out.xlsx
```

Create Excel only for a specific time range:

```cmd
python dump_to_excel_charts.py opensm-statistics.dump -t "Mar 28 09:22:14 ~ Apr 11 17:20:36"
```

Limit charts for a quick test:

```cmd
python dump_to_excel_charts.py opensm-statistics.dump --max-charts 5 -o test.xlsx
```

Show help:

```cmd
python dump_to_excel_charts.py -h
```

## Command Options

```text
usage: dump_to_excel_charts.py [-h] [-o OUTPUT] [-s SHEET] [--max-charts N]
                               [-t TIME_RANGE]
                               [dump_file]

positional arguments:
  dump_file             Path to .dump CSV file
                        default: opensm-statistics.dump

options:
  -h, --help            Show help message and exit
  -o, --output OUTPUT   Output .xlsx path
                        default: <dump stem>_charts.xlsx
  -s, --sheet SHEET     Worksheet name for tabular data
                        default: OpenSM_Statistics
  --max-charts N        Limit to first N numeric columns after TIME_STAMP
  -t, --time-range      Inclusive TIME_STAMP range
                        example: "Nov 02 18:57:30 ~ Jan 15 01:57:30"
```

## Output Workbook

The generated Excel workbook contains:

### 1. OpenSM_Statistics

This sheet contains all filtered raw rows from the dump file.

If `-t` is not used, all rows are written.

### 2. Charts

This sheet contains line charts for each numeric statistics column.

The X-axis is `TIME_STAMP`.

The Y-axis is the raw counter value.

### 3. Delta Charts

This sheet contains line charts based on delta values.

The X-axis is `TIME_STAMP`.

The Y-axis is:

```text
current value - previous value
```

## Notes

The dump timestamp format does not include a year.

Example:

```text
Mar 28 09:22:14
```

For time filtering, the script internally assigns a base year and handles year rollover when the data crosses from one year to the next, such as `Nov` to `Jan`.

Excel still displays the timestamp in the original dump style.
