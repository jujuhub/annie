#!/bin/bash

# Grabs the absorbance at WAVELENGTH, ordered by
# week, and puts it in a .txt file
# Julie He <juhe@ucdavis.edu>


if [ "$#" -ne 2 ]; then
	echo "USAGE: ./abs_grabs.sh [LIST_OF_FILE_EXT.txt] [WAVELENGTH 000.00]"
	exit 1
fi

# remove old files
rm absvt_*

INPUT_FILE="$1"
WAVELENGTH="$2"

while read file_ext; do
	for file in `find ~/ANNIE/Gd_testing/weekly/* -type f -name "File*[0-9]_$file_ext.txt" | sort -t '/' -k 8`; do
		grep "$WAVELENGTH" $file >> absvt_$file_ext.txt

#		echo $file
#		echo "`grep $WAVELENGTH $file`"

	done

	# plot the absorption values over time
#	python plot_abs_t.py absorption_$file_ext.txt $WAVELENGTH $file_ext

done < $INPUT_FILE
