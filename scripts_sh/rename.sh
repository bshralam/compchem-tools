#!/bin/bash

# Loop through all .in files in the directory
for file in *.in; do
  # Check if the filename contains 'basis2'
  if [[ "$file" == *basis2* ]]; then
    # Construct new filename by replacing 'basis2' with 'basis4'
    newfile="${file/basis2/basis4}"

    # Rename the file
    mv "$file" "$newfile"

    echo "Renamed: $file -> $newfile"
  fi
done
