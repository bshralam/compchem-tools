#!/bin/bash

# Usage: ./script.sh file1.in
# Example: ./script.sh opt1.in

# Input file
file1="$1"

# Generate file2 name by replacing "opt" with "freq"
file2="${file1/opt/freq}"

# Step 1: Copy file1.in → file2.in
cp "$file1" "$file2"

# Step 2a: Replace jobname line with file2 name
sed -i "s/^jobname.*/jobname                ${file2}/" "$file2"

# Step 2b: Remove line starting with new_minimizer
sed -i "/^new_minimizer/d" "$file2"

# Step 2c: Insert 'mincheck false' on line 5
sed -i '5i mincheck                false' "$file2"

# Step 2d: Replace word "minimize" with "frequencies"
sed -i 's/\bminimize\b/frequencies/g' "$file2"

echo "File transformation complete: $file1 → $file2"


