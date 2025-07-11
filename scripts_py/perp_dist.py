#!/usr/bin/env python3

import argparse
import numpy as np

def read_xyz(filename):
    with open(filename) as f:
        lines = f.readlines()[2:]  # Skip first two lines of XYZ header
        coords = np.array([list(map(float, line.split()[1:])) for line in lines])
    return coords

def fit_plane(points):
    centroid = points.mean(axis=0)
    _, _, vh = np.linalg.svd(points - centroid)
    normal = vh[-1]
    return centroid, normal

def point_to_plane_distance(point, plane_point, normal):
    return abs(np.dot(point - plane_point, normal)) / np.linalg.norm(normal)

def compute_distance(xyz_file, fullerene_indices, organic_indices):
    coords = read_xyz(xyz_file)
    fullerene_coords = coords[fullerene_indices]
    organic_coords = coords[organic_indices]

    plane_point, normal = fit_plane(organic_coords)
    distances = [point_to_plane_distance(atom, plane_point, normal) for atom in fullerene_coords]
    min_distance = min(distances)
    return min_distance

def parse_indices(index_string):
    indices = []
    parts = index_string.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            indices.extend(range(start - 1, end))  # Convert to 0-based indexing
        else:
            indices.append(int(part) - 1)
    return indices

def main():
    parser = argparse.ArgumentParser(description="Calculate perpendicular distance between molecules from xyz file.")
    parser.add_argument("xyz_file", help="Path to the xyz file")
    parser.add_argument("--fullerene", required=True, help="Indices for fullerene atoms (e.g. 1-60)")
    parser.add_argument("--organic", required=True, help="Indices for organic molecule atoms (e.g. 89-184)")
    
    args = parser.parse_args()

    fullerene_indices = parse_indices(args.fullerene)
    organic_indices = parse_indices(args.organic)

    distance = compute_distance(args.xyz_file, fullerene_indices, organic_indices)
    print(f"Perpendicular distance for {args.xyz_file}: {distance:.3f} Å")

if __name__ == "__main__":
    main()

