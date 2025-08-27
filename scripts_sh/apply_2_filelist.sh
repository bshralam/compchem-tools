#!/bin/bash

# Path to the file containing the list of numbers
NUMBER_LIST="2.numbers.txt"

# Loop through each number in the number list
while IFS= read -r n; do
    # Construct the filename and execute the script
    ./3.arrange.sh "configuration_$n.xyz"
done < "$NUMBER_LIST"

