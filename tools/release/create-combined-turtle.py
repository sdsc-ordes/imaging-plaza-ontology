# TODO: replace python script with rdfpipe / sop
# script.sh onto-dir/ -> cat ontodir/*ttl -> serialize to all formats -> gzip
from rdflib import Graph
import os

# Define the base directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load prefixes
prefixes_graph = Graph()
prefixes_graph.parse(os.path.join(base_dir, "schemas/prefixes.ttl"), format="turtle")

# Load the ontology files
ontology_files = [
    os.path.join(base_dir, "schemas/ImagingOntologyShapes.ttl"),
    os.path.join(base_dir, "schemas/ImagingOntology.ttl"),
    os.path.join(base_dir, "schemas/ImagingOntologyEnumeration.ttl")
]

combined_content = ""

for ontology_file in ontology_files:
    with open(ontology_file, "r") as f:
        combined_content += f.read()

# Remove all prefixes from the combined content
combined_content = "\n".join([line for line in combined_content.split("\n") if not line.startswith("@prefix")])

# Write the combined content to a new file
with open(os.path.join(base_dir, "schemas/combined.ttl"), "w") as f:
    f.write(combined_content)

#prepend prefixes from prefixes.ttl to the new combined file
with open(os.path.join(base_dir, "schemas/ImagingOntologyCombined.ttl"), "w") as f:
    for line in open(os.path.join(base_dir, "schemas/prefixes.ttl")):
        f.write(line)
    f.write("\n")
    f.write(combined_content)

os.remove(os.path.join(base_dir, "schemas/combined.ttl"))


