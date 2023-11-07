"""
Command-line interface to run PyLint on a given directory and check the score against a threshold.
Usage: $ python lint.py --path ./my_project --threshold 8.5
"""

import argparse
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", default="./src", type=str)
parser.add_argument("-t", "--threshold", default=7, type=float)
args = parser.parse_args()

# Linting
pylint_output = StringIO()
results = Run([args.path], reporter=TextReporter(pylint_output), exit=False)

if args.threshold > (score := float(results.linter.stats.global_note)):
    print(f"PyLint Failed | Score: {score} | Threshold: {args.threshold}\n{float(results.linter.stats.global_note)}")
    raise ValueError("PyLint check failed")
print(f"PyLint Passed | Score: {score} | Threshold: {args.threshold}")
