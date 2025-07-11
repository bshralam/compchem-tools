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

# Function to write XYZ file
def write_xyz(filename, atoms1, coords1, atoms2, coords2):
    with open(filename, 'w') as file:
        file.write(f"{len(atoms1) + len(atoms2)}\n")
        file.write("Generated configuration\n")
        for atom, coord in zip(atoms1, coords1):
            file.write(f"{atom} {coord[0]} {coord[1]} {coord[2]}\n")
        for atom, coord in zip(atoms2, coords2):
            file.write(f"{atom} {coord[0]} {coord[1]} {coord[2]}\n")

# Function to calculate the center of mass
def compute_com(atoms, coords):
    masses = {'H': 1.008, 'C': 12.01, 'O': 16.00, 'N': 14.01}  # Add more as needed
    total_mass = sum([masses[atom] for atom in atoms])
    com = sum([masses[atom] * coord for atom, coord in zip(atoms, coords)]) / total_mass
    return com

# Function to generate points on a sphere
def generate_sphere_points(radius, num_points=50):
    points = []
    phi = np.pi * (3. - np.sqrt(5.))  # Golden angle
    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2  # y goes from 1 to -1
        radius_at_y = np.sqrt(1 - y * y)  # radius at y
        theta = phi * i  # golden angle increment
        x = np.cos(theta) * radius_at_y
        z = np.sin(theta) * radius_at_y
        points.append([x, y, z])
    return np.array(points) * radius

# Main function to generate configurations
def generate_configurations(file1, file2, radius, num_points=50):
    atoms1, coords1 = read_xyz(file1)
    atoms2, coords2 = read_xyz(file2)

    # Compute center of mass for molecule 2
    com2 = compute_com(atoms2, coords2)

    # Generate points on the sphere around COM of molecule 2
    sphere_points = generate_sphere_points(radius, num_points)

    # For each point on the sphere, place molecule 1 at that point and output the configuration
    for i, point in enumerate(sphere_points):
        # Translate molecule 1 to the point on the sphere
        translation_vector = point - compute_com(atoms1, coords1)
        new_coords1 = coords1 + translation_vector

        # Write the new configuration to an XYZ file
        output_filename = f"configuration_{i+1}.xyz"
        write_xyz(output_filename, atoms1, new_coords1, atoms2, coords2)
        print(f"Generated configuration {i+1}: {output_filename}")

# Example usage:
# Replace 'molecule1.xyz' and 'molecule2.xyz' with your filenames, and set the desired radius.
generate_configurations('acceptor.xyz', 'donor.xyz', radius=10.0)

