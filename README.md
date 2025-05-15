# hexameric array builder
Script to build the pMMO hexameric array 

python hexarray.py

Then need to add the file to remove the lines
END
TER

# pore lipids builder
Script to build a small cylidrical bilayer in pMMO pore. 

 
# Generate restraits (mdp and ndx)
The first script reads a template MDP file (template.mdp) that contains pull restraints
for one pMMO, and writes a new MDP file with updated pull-group and pull-coord definitions
to account for multiple copie

The second script reads a template index file that defines groups for one unit cell
and writes a new index file with the same groups replicated for each pMMO copy.
Each subsequent copy has its atom indices shifted by the number of atoms per unit.


