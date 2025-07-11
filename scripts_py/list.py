import os
import re

def scan_directory_for_geom_files():
    # List to hold the extracted numbers
    numbers = []
    
    # Iterate through all files in the current directory
    for filename in os.listdir('.'):
        # Check if the file matches the pattern 'geom-*.xyz'
        if re.match(r"geom-\d+\.xyz", filename):
            # Extract the number from the filename using regex
            number = re.search(r"(\d+)", filename)
            if number:
                numbers.append(int(number.group(1)))  # Convert to integer for sorting
    
    # Sort the numbers in ascending order
    numbers.sort()
    
    # Write the numbers to 'numbers.txt' in the current directory
    with open('numbers.txt', 'w') as f:
        f.write("\n".join(map(str, numbers)))

# Run the function to scan the current directory
scan_directory_for_geom_files()

