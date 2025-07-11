#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <filename> <start_line> <end_line>"
    exit 1
fi

filename="$1"
start_line="$2"
end_line="$3"

temp_file="temp_coords.txt"

# Extract specified line range using sed
sed -n "${start_line},${end_line}p" "$filename" > "$temp_file"

# Extract x, y, and z values
x_vals=$(awk '{print $2}' "$temp_file" | sort -n)
y_vals=$(awk '{print $3}' "$temp_file" | sort -n)
z_vals=$(awk '{print $4}' "$temp_file" | sort -n)

# Determine min and max values
x_min=$(echo "$x_vals" | head -1)
x_max=$(echo "$x_vals" | tail -1)
y_min=$(echo "$y_vals" | head -1)
y_max=$(echo "$y_vals" | tail -1)
z_min=$(echo "$z_vals" | head -1)
z_max=$(echo "$z_vals" | tail -1)

# Cleanup
rm "$temp_file"

echo "x_max: $x_max, x_min: $x_min"
echo "y_max: $y_max, y_min: $y_min"
echo "z_max: $z_max, z_min: $z_min"

