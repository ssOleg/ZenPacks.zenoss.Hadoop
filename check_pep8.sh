#!/bin/bash

PY_FILES=$(find . -name '*.py' -not -path "*./ZenPacks/zenoss/Hadoop/lib*" -not -path "*./build*")
python pep8.py --show-source $PY_FILES
