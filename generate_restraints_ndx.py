#!/usr/bin/env python3
"""
This script reads a template index file that defines groups for one unit cell
and writes a new index file with the same groups replicated for each pMMO copy.
Each subsequent copy has its atom indices shifted by the number of atoms per unit.

Update the variable atoms_per_unit to your known value (here 160547).
The script also appends a suffix to the group name for copies 2, 3, etc.
"""

atoms_per_unit = 160547  # number of atoms in one pMMO unit
num_copies = 4           # total number of copies

def shift_indices(indices, offset):
    # Given a list of indices (as strings), add the offset to each integer
    return " ".join(str(int(x) + offset) for x in indices)

# Read the template index file
groups = {}  # dictionary: key = group name, value = list of atom indices (as strings)
current_group = None

with open("template.ndx", "r") as fin:
    for line in fin:
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            current_group = line.strip('[]').strip()
            groups[current_group] = []
        elif current_group and line:
            # Allow numbers on the same line separated by whitespace
            groups[current_group].extend(line.split())

# Write out the new index file
with open("restraints.ndx", "w") as fout:
    for copy in range(num_copies):
        offset = copy * atoms_per_unit
        # For each group in the template, write the shifted group for this copy.
        for group, indices in groups.items():
            # For copy 1, you can use the original name; for others append _2, _3, etc.
            new_group = group if copy == 0 else f"{group}_{copy+1}"
            fout.write(f"[{new_group}]\n")
            shifted = shift_indices(indices, offset)
            fout.write(f"{shifted}\n\n")

print("New replicated index file saved as new_index.ndx")
