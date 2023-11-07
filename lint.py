"""
Command-line interface to run PyLint on a given directory and check the score against a threshold.
Usage: $ python lint.py --path ./my_project --threshold 8.5
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
PATH = str(args.path)
THRESHOLD = float(args.threshold)

logging.info("PyLint Starting | Path: %s | Threshold: %s", PATH, THRESHOLD)

pylint_output = StringIO()  # Custom open stream
reporter = TextReporter(pylint_output)
results = Run([PATH], reporter=reporter, exit=False)


final_score = results.linter.stats.global_note

if float(final_score) < THRESHOLD:
    message = f"PyLint Failed | Score: {final_score} | Threshold: {THRESHOLD}"
    logging.error(message)
    print(pylint_output.getvalue())
    raise ValueError(message)
else:
    message = f"PyLint Passed | Score: {final_score} | Threshold: {THRESHOLD}"
    logging.info(message)
    sys.exit(0)
