# OpenSM Statistics Dump to Excel Charts

## Intro

This script reads an `opensm-statistics.dump` file from OpenSM and creates an Excel workbook with raw statistics, normal charts, and delta charts.

It is useful when you want to quickly visualize OpenSM MAD counter changes over time 

## Main Features

- Reads `opensm-statistics.dump` CSV data.
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


## Delta Chart Meaning

The `Delta Charts` sheet calculates the difference between the current row and the previous row for each numeric column.
 It's very useful to see if when there were MAD spike or weird data spike.

Example with `LIGHT_SWEEP_COUNT`:

```text
Raw data:
3747077
3747438
3747799
...

Delta data : (Current data - Previous time data)
(3747438 - 3747077) = 361
(3747799 - 3747438) = 361
...

```


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

## Excel capture as a result

> Accumulated chart 
<img width="1108" height="306" alt="Image" src="https://github.com/user-attachments/assets/8058c68d-745b-404c-95b0-e07c6324eec9" />

> Delta chart 
<img width="1109" height="304" alt="Image" src="https://github.com/user-attachments/assets/34254ec9-6005-4930-b40b-0417e52827d7" />