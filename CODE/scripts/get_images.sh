#!/bin/bash
for i in {1..100}; do
    mkdir $i
    cd $i
    python3 ../../scripts/download.py -i $i -r $((i + 1))  -z
    rm -rf images
    rm *.json
    rm manifest.txt
    cd ..
done