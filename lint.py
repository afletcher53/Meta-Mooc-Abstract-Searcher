"""
This module provides a command-line interface to run PyLint on a given directory and 
check the resulting score against a threshold.

The module defines an argument parser that accepts two optional arguments:
- `path`: the path to the directory to be linted (default: "./src")
- `threshold`: the minimum score required to pass the linting (default: 7)

The module uses PyLint's `Run` function to lint the specified directory and generate 
a score report. If the final score is below the threshold, the module raises an exception 
and prints the score report to the console. Otherwise, it exits with a success status code.

Example usage:
    $ python lint.py --path ./my_project --threshold 8.5
"""


import argparse
import logging
import sys
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter

logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser(prog="LINT")

parser.add_argument(
    "-p",
    "--path",
    help="path to directory you want to run pylint | "
    "Default: %(default)s | "
    "Type: %(type)s ",
    default="./src",
    type=str,
)

parser.add_argument(
    "-t",
    "--threshold",
    help="score threshold to fail pylint runner | "
    "Default: %(default)s | "
    "Type: %(type)s ",
    default=7,
    type=float,
)

args = parser.parse_args()
path = str(args.path)
threshold = float(args.threshold)

logging.info("PyLint Starting | Path: %s | Threshold: %s", path, threshold)

pylint_output = StringIO()  # Custom open stream
reporter = TextReporter(pylint_output)
results = Run([path], reporter=reporter, exit=False)


final_score = results.linter.stats.global_note

if float(final_score) < threshold:
    message = f"PyLint Failed | Score: {final_score} | Threshold: {threshold}"
    logging.error(message)
    print(pylint_output.getvalue())
    raise ValueError(message)
else:
    message = f"PyLint Passed | Score: {final_score} | Threshold: {threshold}"
    logging.info(message)
    sys.exit(0)
