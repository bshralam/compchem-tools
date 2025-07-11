import numpy as np
import argparse

def read_xyz(filename):
    """Reads the .xyz file and returns atom symbols and coordinates."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Skip the first two lines (atom count and comment)
        atom_count = int(lines[0].strip())
        coordinates = []
        
        for line in lines[2:]:
            parts = line.split()
            symbol = parts[0]
            x, y, z = map(float, parts[1:])
            coordinates.append((symbol, np.array([x, y, z])))
            
    return atom_count, coordinates

def closest_distance_between_segments(coordinates, n):
    """Calculates the closest distance between two segments starting from index n."""
    min_distance = float('inf')
    closest_pair = None
    
    # Split into two segments
    segment1 = coordinates[:n]
    segment2 = coordinates[n:]
    
    # Calculate pairwise distances
    for atom1, coord1 in segment1:
        for atom2, coord2 in segment2:
            distance = np.linalg.norm(coord1 - coord2)
            if distance < min_distance:
                min_distance = distance
                closest_pair = (atom1, atom2, coord1, coord2)
    
    return min_distance, closest_pair

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Calculate the closest distance between two segments in an .xyz file.")
    parser.add_argument("filename", type=str, help="Path to the .xyz file")
    parser.add_argument("n", type=int, help="Index where the second molecule starts")

    # Parse arguments
    args = parser.parse_args()
    filename = args.filename
    n = args.n

    # Read the file and calculate the closest distance
    atom_count, coordinates = read_xyz(filename)
    min_distance, closest_pair = closest_distance_between_segments(coordinates, n)

    # Print results
    print(f"The closest distance is {min_distance:.4f} Å")
    print(f"Between atoms: {closest_pair[0]} at {closest_pair[2]} and {closest_pair[1]} at {closest_pair[3]}")

if __name__ == "__main__":
    main()

