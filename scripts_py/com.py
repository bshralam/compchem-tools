import numpy as np

# Function to read XYZ files and return atom symbols and coordinates
def read_xyz(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines (comment and atom count)
    atoms = []
    coords = []
    for line in lines:
        parts = line.split()
        atoms.append(parts[0])
        coords.append([float(x) for x in parts[1:4]])
    return atoms, np.array(coords)

# Function to calculate the center of mass
def compute_com(atoms, coords):
    masses = {'H': 1.008, 'C': 12.01, 'O': 16.00, 'N': 14.01}  # Add more elements as needed
    total_mass = sum([masses[atom] for atom in atoms])
    com = sum([masses[atom] * coord for atom, coord in zip(atoms, coords)]) / total_mass
    return com

# Function to calculate the distance between the COM of two molecules
def compute_com_distance(config_file):
    atoms, coords = read_xyz(config_file)

    # Split the atoms and coordinates into two molecules (assuming equal length halves)
#    half_len = len(atoms) // 2
    atoms1, coords1 = atoms[:72], coords[:72]
    atoms2, coords2 = atoms[72:], coords[72:]

    # Compute the COM for both molecules
    com1 = compute_com(atoms1, coords1)
    com2 = compute_com(atoms2, coords2)

    # Compute the distance between the two COMs
    distance = np.linalg.norm(com1 - com2)
    return distance

# Main function to read configuration indices and calculate distances
def compute_distances_from_file(index_file):
    with open(index_file, 'r') as file:
        indices = file.readlines()
    
    distances = []
    for index in indices:
        index = index.strip()
        config_file = f"geom-{index}.xyz"
        try:
            distance = compute_com_distance(config_file)
            distances.append((config_file, distance))
            print(f"COM Distance for {config_file}: {distance:.3f} Å")
        except FileNotFoundError:
            print(f"File {config_file} not found. Skipping.")
    
    return distances

# Example usage
index_file = 'numbers.txt'  # Replace with your file containing indices
distances = compute_distances_from_file(index_file)

# Optionally, write results to a file
with open('com_distances.txt', 'w') as output_file:
    for config_file, distance in distances:
        output_file.write(f"{config_file}: {distance:.3f} Å\n")

