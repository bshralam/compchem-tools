import numpy as np

def read_xyz(file_path, n):
    #Read coordinates from .xyz file and separates into two molecules.
    coords = []
    with open(file_path, 'r') as file:
        # Skip first two lines
        file.readline()
        file.readline()
        for line in file:
            parts = line.split()
            if len(parts) >= 4:
                # Skip atomic symbols
                x, y, z = map(float, parts[1:4])
                coords.append((x, y, z))

    mol1_coords = coords[:n]
    mol2_coords = coords[n:]
    return mol1_coords, mol2_coords

def center_of_mass(coords):
    #Returns COM of a molecule
    coords = np.array(coords)
    num_atoms = len(coords)
    COM = np.sum(coords, axis=0) / num_atoms
    return tuple(COM)

def distance(point1, point2):
   #Euclidean distance between two points

    point1 = np.array(point1)
    point2 = np.array(point2)
    dist = np.linalg.norm(point1 - point2)
    return dist

file_path = 'optimized.xyz'
natoms_mol1 = 12
mol1_coords, mol2_coords = read_xyz(file_path, natoms_mol1)
COM_mol1 = center_of_mass(mol1_coords)
COM_mol2 = center_of_mass(mol2_coords)
dist = distance(COM_mol1, COM_mol2)
print(f"Distance between the molecules: {dist}")
