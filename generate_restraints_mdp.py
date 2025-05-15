#!/usr/bin/env python3
"""
This script reads a template MDP file (template.mdp) that contains pull restraints
for one pMMO, and writes a new MDP file with updated pull-group and pull-coord definitions
to account for multiple copies.

The template file must define:
  - pull-ncoords and pull-ngroups,
  - Lines starting with 'pull-groupX-name = ...'
  - Lines starting with 'pull-coordX-' for properties like type, geometry, dim, groups, init, rate, k, etc.

It will replicate each such line for every copy, shifting:
  - Group numbers by (copy_index * orig_ngroups)
  - Coord indices by (copy_index * orig_ncoords)

Please update the variables below if your numbers differ.
"""
import re

num_copies = 4
orig_ngroups = 39   # from your template.mdp
orig_ncoords = 30   # from your template.mdp

# Read the template MDP file into a list of lines
with open("template.mdp", "r") as f:
    lines = f.readlines()

new_lines = []
# We will need to modify the pull-ncoords and pull-ngroups lines:
for line in lines:
    if re.match(r"^\s*pull\-ngroups", line):
        new_ngroups = orig_ngroups * num_copies
        new_lines.append(f"pull-ngroups = {new_ngroups}\n")
    elif re.match(r"^\s*pull\-ncoords", line):
        new_ncoords = orig_ncoords * num_copies
        new_lines.append(f"pull-ncoords = {new_ncoords}\n")
    # For lines starting with "pull-group<some_number>-name"
    elif re.match(r"^\s*pull-group(\d+)-name", line):
        m = re.match(r"^\s*pull-group(\d+)-name\s*=\s*(\S+)", line)
        if m:
            orig_index = int(m.group(1))
            orig_name = m.group(2)
            for i in range(num_copies):
                new_index = orig_index + i * orig_ngroups
                # Optionally, append a suffix for copies > 1
                new_name = orig_name if i == 0 else f"{orig_name}_{i+1}"
                new_lines.append(f"pull-group{new_index}-name = {new_name}\n")
        else:
            new_lines.append(line)
    # For lines starting with "pull-coord" definitions
    elif re.match(r"^\s*pull\-coord(\d+)-", line):
        m = re.match(r"^\s*pull\-coord(\d+)(-.*)", line)
        if m:
            orig_coord_index = int(m.group(1))
            suffix = m.group(2)
            # If this line is the "groups" type, we need to shift the numbers inside.
            if suffix.startswith("-groups"):
                # Expecting a line like: "pull-coordX-groups = G1 G2"
                parts = line.split("=")
                lhs = parts[0].strip()  # e.g., pull-coord1-groups
                rhs = parts[1].strip()  # e.g., "1 2"
                group_nums = rhs.split()
                for i in range(num_copies):
                    new_coord_index = orig_coord_index + i * orig_ncoords
                    new_group_nums = []
                    for gn in group_nums:
                        try:
                            new_gn = int(gn) + i * orig_ngroups
                            new_group_nums.append(str(new_gn))
                        except ValueError:
                            new_group_nums.append(gn)
                    new_lines.append(f"pull-coord{new_coord_index}-groups = {' '.join(new_group_nums)}\n")
            else:
                # For all other pull-coord lines (type, geometry, dim, init, etc.), simply replicate them
                for i in range(num_copies):
                    new_coord_index = orig_coord_index + i * orig_ncoords
                    new_lines.append(f"pull-coord{new_coord_index}{suffix}\n")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("dist_restraints.mdp", "w") as fout:
    fout.writelines(new_lines)

print("New MDP file saved as dist_restraints.mdp")
