#!/bin/bash
#SBATCH --time=012:60:00
#SBATCH --nodes=1
#SBATCH --mem=100G
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --partition=cpuq
#SBATCH --job esp1-4

module load Q-Chem/6.1

qchem -nt 32 esp1-4.in esp1-4.out

