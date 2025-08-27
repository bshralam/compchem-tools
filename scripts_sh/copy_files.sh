#!/bin/bash

# Path to the file containing the list of numbers
NUMBER_LIST="2a.numbers.txt"

# Loop through each number in the number list
while IFS= read -r n; do
    # Execute the copy command, creating optn.in for each n
    cp opt-coup.in "opt-coup$n.in"
    #sed -n '3,186p' ../"configuration_$n.xyz" | sed '2r /dev/stdin' "opt$n.in" > temp && mv temp "opt$n.in"
done < "$NUMBER_LIST"

