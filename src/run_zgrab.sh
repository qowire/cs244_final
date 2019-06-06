#!/bin/bash
mkdir ~/inputs
mkdir ~/outputs
INPUT_FILES=~/inputs/*
OUTPUT_FILES=~/outputs/
for f in $INPUT_FILES;
do
	fname="${f##*/}"
	o_file="$OUTPUT_FILES$fname.txt"
	echo "Running ZGrab for inputs $f to $o_file"
	$GOPATH/src/github.com/zmap/zgrab2/zgrab2 -f $f -o $o_file tls
done
