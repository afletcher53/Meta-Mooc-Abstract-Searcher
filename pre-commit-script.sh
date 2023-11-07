#!/bin/bash
echo $"#/bin/sh\nblack .\npython lint.py -p ../Meta-Mooc-Abstract-Searcher/"> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit