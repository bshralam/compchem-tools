#!/bin/bash

insert_file="lines.txt"  # Change this to the file containing lines to insert
directory="."  # Set this to the target directory if needed
pattern="esp1-*.in"

temp_file="temp_marcus_insertion.tmp"

for file in $directory/$pattern; do
    if [[ -f "$file" ]]; then
        awk -v insert_file="$insert_file" 'NR==195 {print; while (getline < insert_file) print; next} 1' "$file" > "$temp_file" && mv "$temp_file" "$file"
        echo "Processed: $file"
    fi
done

