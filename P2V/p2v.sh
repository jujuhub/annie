#!/bin/bash

for filename in ./*charges.txt; do
    python p2v.py "$filename"
done
