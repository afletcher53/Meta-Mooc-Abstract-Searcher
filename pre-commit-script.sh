#!/bin/bash
> .git/hooks/pre-commit
echo $"#/bin/sh" >> .git/hooks/pre-commit
echo $"black ." >> .git/hooks/pre-commit
echo $"python lint.py -p ../Meta-Mooc-Abstract-Searcher/" >> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit