# Near Earth Object Database

The Near Earth Object database is a searchable Python 3 command-line interface (CLI) project.

# Install

A Python 3.6+ project, no external dependencies are required as all libraries used are a part of the Python standard library.

If you have multiple versions of Python installed on your machine, please be mindful [to set up a virtual environment with Python 3.6+](https://docs.python.org/3/library/venv.html).

## To Setup a Python 3  Virtual  Environment

```python3 -m venv /path/to/new/virtual/environment```

# Usage

To use the project:

1. Clone the project to your local machine
2. Create a virtual environment, named `env`, with `python3 -m env /env` in project root
3. Activate the virtual environment with `source env/bin/activate`
4. Navigate to the `/starter` directory
5. Run `python main.py -h` or `./main.py -h` for an explanation of how to run the project
6. Or try it out yourself!

Example of how to use the interface:

1. Find up to 10 NEOs on Jan 1, 2020 displaying output to terminal

`./main.py display -n 10 --date 2020-01-01`

2. Find up to 10 NEOs from input file 'new_neo_data.csv' between Jan 1, 2020 and Jan 10, 2020 within 5 km from Earth,
exporting to a csv file

`./main.py csvfile -n 10 -f new_neo_data.csv --start_date 2020-01-01 --end_date 2020-01-10 --filter distance:>=:5`

