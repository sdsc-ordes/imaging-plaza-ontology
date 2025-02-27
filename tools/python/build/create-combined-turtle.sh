# TODO: replace python script with rdfpipe / sop
# script.sh onto-dir/ -> cat ontodir/*ttl -> serialize to all formats -> gzip

#!/bin/bash

# Check if an argument (ontology directory) is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <ontology-directory>"
    exit 1
fi

ONTO_DIR="$1/src/imaging-ontology"
OUTPUT_DIR="build"
COMBINED_FILE="$OUTPUT_DIR/ontology_combined.ttl"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Concatenate all TTL files in the directory
cat "$ONTO_DIR"/*.ttl > "$COMBINED_FILE"

# Define output formats
FORMATS=("json-ld" "nt" "turtle")

# Convert to multiple formats using rdfpipe and create a single gzip
for format in "${FORMATS[@]}"; do
    python -m rdflib.tools.rdfpipe -i turtle -o "$format" "$COMBINED_FILE" > "$OUTPUT_DIR/ontology_combined.$format"
    echo "Generated: $OUTPUT_DIR/ontology_combined.$format"
done


# replace any string "schema1" in the combined file with "schema" line by line
sed -i 's/schema1/schema/g' $OUTPUT_DIR/ontology_combined.$format

# remove ontology_combined.ttl
rm "$COMBINED_FILE"

# Create a tar.gz archive with all the formats
tar -czf "$OUTPUT_DIR/ontology_combined_formats.tar.gz" -C "$OUTPUT_DIR" .


echo "All conversions and compressions completed."
