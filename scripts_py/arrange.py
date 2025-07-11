def rearrange_lines(input_file, output_file, order):
    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Strip whitespace and create a list of lines
    lines = [line.strip() for line in lines]

    # Rearranging lines according to the specified order
    rearranged_lines = []
    for line_range in order:
        start, end = line_range
        rearranged_lines.extend(lines[start-1:end])  # Adjust for zero-based index

    # Write the rearranged lines to the output file
    with open(output_file, 'w') as file:
        for line in rearranged_lines:
            file.write(line + '\n')

    print("File has been rearranged and saved as", output_file)

# Define the input and output file paths
input_file = 'sp9.in'   # Change this to your input file name
output_file = 'sp9.txt'  # Change this to your desired output file name

# Define the order of lines using ranges (start, end)
# Example: [(1, 2), (6, 8), (3, 5), (9, 10), (11, 11)]
order = [
    (1, 2),   # 1 and 2
    (91, 162),   # 6, 7, and 8
    (3, 90),   # 3, 4, and 5
    (163, 178),  # 9 and 10
]

# Call the function to rearrange lines
rearrange_lines(input_file, output_file, order)

