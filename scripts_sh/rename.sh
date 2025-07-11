#!/bin/bash

# Read number from file
read -r -a numbers < number.txt

# Loop through files matching the pattern marcusX-N.in
for num in "${numbers[@]}"; do
 for file in marcus1-${number}.in; do
    if [[ -f "$file" ]]; then
        new_file="${file/marcus/esp}"
        mv "$file" "$new_file"
        echo "Renamed: $file -> $new_file"
    fi
 done
done
