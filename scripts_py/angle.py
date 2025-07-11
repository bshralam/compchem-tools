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

# Function to calculate the moment of inertia tensor
def inertia_tensor(atoms, coords):
    masses = {'H': 1.008, 'C': 12.01, 'O': 16.00, 'N': 14.01}  # Add more elements as needed
    I = np.zeros((3, 3))
    for atom, coord in zip(atoms, coords):
        mass = masses[atom]
        x, y, z = coord
        I[0, 0] += mass * (y**2 + z**2)
        I[1, 1] += mass * (x**2 + z**2)
        I[2, 2] += mass * (x**2 + y**2)
        I[0, 1] -= mass * x * y
        I[0, 2] -= mass * x * z
        I[1, 2] -= mass * y * z
    I[1, 0] = I[0, 1]
    I[2, 0] = I[0, 2]
    I[2, 1] = I[1, 2]
    return I

# Function to compute the principal axes (eigenvectors) from the moment of inertia tensor
def compute_principal_axes(atoms, coords):
    I = inertia_tensor(atoms, coords)
    eigenvalues, eigenvectors = np.linalg.eigh(I)  # Compute eigenvectors (principal axes)
    return eigenvectors  # Each column is a principal axis

# Function to calculate the angle between two vectors
def compute_angle_between_vectors(v1, v2):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    cosine_angle = np.dot(v1, v2)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))  # Clip to avoid numerical issues
    return np.degrees(angle)

# Main function to compute the orientation angle between two molecules
def compute_orientation_angle(config_file):
    atoms, coords = read_xyz(config_file)

    # Split the atoms and coordinates into two molecules (first 100 atoms for molecule 1, next 60 atoms for molecule 2)
    atoms1, coords1 = atoms[:72], coords[:72]
    atoms2, coords2 = atoms[72:], coords[72:]

    # Compute principal axes for both molecules
    principal_axes1 = compute_principal_axes(atoms1, coords1)
    principal_axes2 = compute_principal_axes(atoms2, coords2)

    # Take the primary principal axis (e.g., first eigenvector) of both molecules
    primary_axis1 = principal_axes1[:, 0]  # First column is the primary axis
    primary_axis2 = principal_axes2[:, 0]

    # Compute the angle between the two primary axes
    angle = compute_angle_between_vectors(primary_axis1, primary_axis2)
    return angle

# Function to loop over multiple configuration files
def compute_angles_from_file(index_file):
    with open(index_file, 'r') as file:
        indices = file.readlines()
    
    angles = []
    for index in indices:
        index = index.strip()
        config_file = f"geom-{index}.xyz"
        try:
            angle = compute_orientation_angle(config_file)
            angles.append((config_file, angle))
            print(f"Orientation angle for {config_file}: {angle:.3f} degrees")
        except FileNotFoundError:
            print(f"File {config_file} not found. Skipping.")
    
    return angles

# Example usage
index_file = 'numbers.txt'  # Replace with your file containing indices
angles = compute_angles_from_file(index_file)

# Optionally, write results to a file
with open('orientation_angles.txt', 'w') as output_file:
    for config_file, angle in angles:
        output_file.write(f"{config_file}: {angle:.3f} degrees\n")

