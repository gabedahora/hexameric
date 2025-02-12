from Bio.PDB import PDBParser, PDBIO
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Structure import Structure

# Define the lattice constant
a = 9.4  # in nm
a *= 10  # convert to Å

# Define the transformation vectors
transformations = [
    (0, 0, 0),  # original position
    (a, 0, 0),  # move by a along x
    (0.5*a, 0.5*a*3**0.5, 0),  # move by c along x and b along y
    (1.5*a, 0.5*a*3**0.5, 0)  # move by a+c along x and b along y
]

# Initialize a new structure
new_structure = Structure("New Structure")

# Parse each PDB file and add it to the new structure
for i, filename in enumerate(["protein_CU1.pdb", "protein_CU2.pdb", "protein_CU3.pdb", "protein_CU4.pdb"]):
    # Parse the PDB file
    parser = PDBParser()
    structure = parser.get_structure("Protein", filename)

    # Apply the transformation
    tx, ty, tz = transformations[i]
    for atom in structure.get_atoms():
        x, y, z = atom.get_coord()
        atom.set_coord((x+tx, y+ty, z+tz))

    # Add the transformed structure to the new structure
    model = Model(i)
    for chain in structure.get_chains():
        new_chain = Chain(chain.id)
        for residue in chain.get_residues():
            new_chain.add(residue)
        model.add(new_chain)
    new_structure.add(model)

# Write the new structure to a PDB file
io = PDBIO()
io.set_structure(new_structure)
io.save("hexameric_array.pdb")
