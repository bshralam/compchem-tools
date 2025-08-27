#!/bin/bash

# Check if the file is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

# Assign the file to a variable
file="$1"

# Use sed to cut lines 3-62 and paste them after line 162
sed -i -e '3,90d' -e '186r /dev/stdin' "$file" < <(sed -n '3,90p' "$file")

echo "Lines 3 to 90 have been cut from the original file and inserted after line 162 in $file."

