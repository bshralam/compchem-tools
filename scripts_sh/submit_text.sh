
# File containing the list of words
WORD_LIST="words.txt"

# Read words into an array
mapfile -t words < "$WORD_LIST"

# Loop through the words in pairs
for (( i=0; i<${#words[@]}-1; i++ )); do
    w1=${words[i]}
    w2=${words[i+1]}
    
    # Replace first occurrence of w1 with w2 in qchem.sh
    sed -i "s/\b${w1}\b/${w2}/g" qchem.sh

    # Submit the job
    sbatch qchem.sh
done
