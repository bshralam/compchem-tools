#!/bin/bash

# Define the energy terms to extract
TERMS="E_elec|E_pauli|E_disp|E_cls_elec|E_mod_pauli|E_pct|E_HO|POLARIZATION|CHARGE TRANSFER"

# Read each number from numbers.txt
while IFS= read -r NUM; do
    # Define the input and output files dynamically based on the number
    FILE="marcus2-$NUM.out"
    OUTPUT_FILE="marcus2-$NUM-eda.out"

    # Check if the input file exists
    if [[ ! -f "$FILE" ]]; then
        echo "Input file $FILE does not exist"
        continue
    fi

    # Clear the output file before writing
    > "$OUTPUT_FILE"

    # Extract and save the values
    while IFS= read -r line; do
        if [[ $line =~ ($TERMS) ]]; then
            key=$(echo "$line" | grep -oE "($TERMS)")
            value=$(echo "$line" | sed -E 's/.*= *([-+]?[0-9]*\.?[0-9]+)/\1/')
            echo "$key: $value" >> "$OUTPUT_FILE"
        fi
    done < "$FILE"

    # Print completion message for this file
    echo "Extracted values saved to $OUTPUT_FILE"
done < "numbers.txt"

