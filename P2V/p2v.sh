#!/bin/bash
# need to have this script in dir with all charges.txt

if [ `ls -1 ./*peak2valley.txt 2>/dev/null | wc -l ` -gt 0 ]; then
    echo "These files already exist. Removing.."
    rm *peak2valley.txt
else
    echo "These files don't exist. GTFO."
fi

for filename in *charges.txt; do
    # affects python script condition for writing to diff files
    python p2v.py "$filename"
done
