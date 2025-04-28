# TODO: replace python script with rdfpipe / sop
# script.sh onto-dir/ -> cat ontodir/*ttl -> serialize to all formats -> gzip

#!/bin/bash
# Define an associative array for format to extension mapping
declare -A fmt2ext=(
    ["turtle"]="ttl"
    ["json-ld"]="jsonld"
    ["nt"]="nt"
)
# Check if an argument (ontology directory) is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <ontology-directory>"
    exit 1
fi

ONTO_DIR="$1"
OUTPUT_DIR="build"
COMBINED_FILE="$OUTPUT_DIR/ontology_combined_init.ttl"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Concatenate all TTL files in the directory
for file in "$ONTO_DIR"/*.ttl; do
    cat "$file" >> "$COMBINED_FILE"
    echo "" >> "$COMBINED_FILE"
done

# Define output formats
FORMATS=("json-ld" "nt" "turtle")

# Convert to multiple formats using rdfpipe and create a single gzip
for format in "${FORMATS[@]}"; do
ext=${fmt2ext[$format]}
    python -m rdflib.tools.rdfpipe -i turtle -o "$format" "$COMBINED_FILE" > "$OUTPUT_DIR/ontology_combined.$ext"
    echo "Generated: $OUTPUT_DIR/ontology_combined.$ext"
done


# replace any string "schema1" in the combined file with "schema" line by line
sed -i 's/schema1/schema/g' $OUTPUT_DIR/ontology_combined.$ext

# remove ontology_combined.ttl
rm "$COMBINED_FILE"

# Create a tar.gz archive with all the formats
tar -czf "$OUTPUT_DIR/ontology_combined_formats.tar.gz" -C "$OUTPUT_DIR" .


echo "All conversions and compressions completed."
