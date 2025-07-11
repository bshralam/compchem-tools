import numpy as np
import sys
import os

def read_xyz(file_path):
    """Reads an XYZ file and extracts atomic coordinates."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    atom_count = int(lines[0].strip())  # First line is the number of atoms
    coordinates = []
    for line in lines[2:2 + atom_count]:  # Coordinates start from line 3 (index 2)
        _, x, y, z = line.split()  # Split each line into atom type and coordinates
        coordinates.append([float(x), float(y), float(z)])  # Convert to floats
    return np.array(coordinates)

def calculate_distances(coords1, coords2, exclude_indices1, exclude_indices2):
    """Calculates distances between atoms of two molecules, excluding specified atoms."""
    min_distance = float('inf')
    closest_pair = (-1, -1)
    
    # Exclude atoms from the comparison based on the given indices
    for i, atom1 in enumerate(coords1):
        if i in exclude_indices1:
            continue  # Skip atoms to be excluded
        
        for j, atom2 in enumerate(coords2):
            if j in exclude_indices2:
                continue  # Skip atoms to be excluded

            distance = np.linalg.norm(atom1 - atom2)
            if distance < min_distance:
                min_distance = distance
                closest_pair = (i + 1, j + len(coords1) + 1)  # Adjusting indices for human readability
    return min_distance, closest_pair

# Accept the exclusion indices file as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python dist_sep.py <exclude_indices_file>")
    sys.exit(1)

exclude_indices_file = sys.argv[1]

# Read the list of excluded atom indices
with open(exclude_indices_file, 'r') as f:
    exclude_indices = [int(line.strip()) - 1 for line in f.readlines()]  # Convert to zero-indexed

if not exclude_indices:
    print("No atoms excluded. All atoms will be considered in the distance calculation.")

# Read the numbers from numbers.txt to get the filenames
with open('numbers.txt', 'r') as f:
    numbers = [line.strip() for line in f.readlines()]

if not numbers:
    print("Warning: numbers.txt is empty. No files to process.")
    sys.exit(1)  # Exit the script if no files are listed in numbers.txt

# Output file
output_file = 'distances_output.txt'

# Iterate over the numbers and process each corresponding geom-*.xyz file
for number in numbers:
    file_path = f"geom-{number}.xyz"
    
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found. Skipping.")
        continue
    
    # Read coordinates from the XYZ file
    coordinates = read_xyz(file_path)

    # Split into two molecules (define molecule sizes here)
    molecule1_size = 72  # Adjust size of molecule 1 as needed
    molecule2_size = len(coordinates) - molecule1_size  # Remaining atoms belong to molecule 2

    molecule1_coords = coordinates[:molecule1_size]
    molecule2_coords = coordinates[molecule1_size:]

    # Define the exclusion indices for both molecules (if any)
    exclude_indices1 = [i for i in exclude_indices if i < molecule1_size]
    exclude_indices2 = [i for i in exclude_indices if i >= molecule1_size]  # Adjust for molecule 2

    # Calculate the shortest distance excluding specified atoms
    shortest_distance, (atom1_index, atom2_index) = calculate_distances(molecule1_coords, molecule2_coords, exclude_indices1, exclude_indices2)

    # Output the result to a file (single line)
    with open(output_file, 'a') as f:
        f.write(f"{file_path} | Shortest distance: {shortest_distance:.4f} Å | Closest atoms: Molecule 1 Atom {atom1_index}, Molecule 2 Atom {atom2_index}\n")

    print(f"Processed {file_path}. Results written to {output_file}")

