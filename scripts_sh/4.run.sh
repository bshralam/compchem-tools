#!/bin/bash

# Path to the file containing the list of numbers
NUMBER_LIST="numbers.txt"

# Read the numbers into an array
mapfile -t numbers < "$NUMBER_LIST"

# Loop through the numbers in pairs
for (( i=0; i<${#numbers[@]}-1; i++ )); do
    n1=${numbers[i]}
    n2=${numbers[i+1]}
    
    # Execute the sed command to substitute optn1 with optn2
    sed -i "s/marcus2-${n1}/marcus2-${n2}/g" qchem.sh
    
    # Execute sbatch qchem.sh
    sbatch qchem.sh
done

