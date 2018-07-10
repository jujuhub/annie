#!/bin/bash

# Creates ROOT macros for plotting
# Julie He <juhe@ucdavis.edu>

if [ "$#" -ne 2 ]; then
	echo "USAGE: ./spectra.sh [LIST_OF_EXT.txt] [COLOR_FILE.txt]"
	exit 1
fi

INPUT_FILE="$1"
COLOR_FILE="$2"

while read ext; do
	# create list of spectrum .txt files for each material ($ext)
	find ~/ANNIE/Gd_testing/weekly/* -type f -name "File*[0-9]_$ext.txt" | sort -t '/' -k 8 > flist_$ext.txt

	# create root macro for $ext; find better way of writing to macro
	echo "#include \"TGraph.h\"" > specplots_$ext.C
	echo -e "#include \"TLegend.h\"\n" >> specplots_$ext.C

	echo -e "void specplots_$ext()\n{" >> specplots_$ext.C
	echo -e "    TLegend* legend = new TLegend(0.78, 0.7, 0.93, 0.93);\n" >> specplots_$ext.C

	i=0
	for file in `find ~/ANNIE/Gd_testing/weekly/* -type f -name "File*[0-9]_$ext.txt" | sort -t '/' -k 8`; do
		echo "    TGraph* g$i = make_spect_graph(\"$file\");" >> specplots_$ext.C
		echo -e "    legend->AddEntry(g$i, \"`echo $file | cut -f 8 -d '/' | cut -f 2 -d '_' | sed 's_\([0-9]\{2\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)_20\1-\2-\3_'`\", \"l\");\n" >> specplots_$ext.C
		((i++))
	done

#	while read file; do
#		echo "		TGraph* g$i = make_spect_graph(\"$file\");" >> specplots_$ext.C
#		echo -e "    legend->AddEntry(g$i, \"2017 `ls -l $file | awk '{print $6,$7;}'`\", \"l\");\n" >> specplots_$ext.C
#		((i++))
#	done < flist_$ext.txt

	echo -e "    g0->SetTitle(\"$ext\");" >> specplots_$ext.C
	j=1
	while read color && [ $j -lt `wc -l flist_$ext.txt | awk '{print $1;}'` ]; do
		echo "    g$j->SetLineColor($color);" >> specplots_$ext.C
		((j++))
	done < $COLOR_FILE

	echo -e "\n    g0->Draw();" >> specplots_$ext.C
	k=1
	while [ $k -lt `wc -l flist_$ext.txt | awk '{print $1;}'` ]; do
		echo "    g$k->Draw(\"same\");" >> specplots_$ext.C
		((k++))
	done

	echo -e "\n    legend->Draw();\n\n}\n" >> specplots_$ext.C

	echo -e "int main()\n{\n    specplots_$ext();\n    return 0;\n}" >> specplots_$ext.C
done < $INPUT_FILE
