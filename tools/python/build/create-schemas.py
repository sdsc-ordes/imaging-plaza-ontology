import rdflib
import json
from pathlib import Path
import argparse


def generate_schema_graph(turtle_file: Path) -> rdflib.Graph:
    """
    Generate rdflib.Graph from a Turtle file.

    Args:
        turtle_file: The path to the Turtle file.

    Returns:
        The rdflib.Graph object containing the data.
    """
    data_g = rdflib.Graph()
    data_g.parse(turtle_file, format="turtle")
    return data_g


def extract_labels_and_placeholders(data_g: rdflib.Graph) -> dict:
    """
    Extract labels and placeholders from rdflib.Graph.

    Args:
        data_g: The rdflib.Graph object containing the data.

    Returns:
        The extracted labels and placeholders as a dictionary.
    """
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?iri ?label ?comment
    WHERE {
        {
            ?iri rdfs:label ?label .
        }
        UNION
        {
            ?iri rdfs:comment ?comment .
        }
    }
    """
    result = data_g.query(query)
    schema_json = {
        "@type_label": "Type",
        "add_modal_button": "Add {{type}}",
        "publish": "Publish",
        "published": "Published!",
        "save-draft": "Save draft",
        "value": "Value",
        "general_table_action": "Action",
    }
    for row in result:
        iri = str(row.iri)
        slug = iri.split("/")[-1].split("#")[-1]
        if row.label:
            schema_json[f"{slug}_label"] = str(row.label)
        if row.comment:
            schema_json[f"{slug}_placeholder"] = str(row.comment)
    return schema_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract labels and placeholders from ontology TTL file.")
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the input Turtle (.ttl) file."
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path to the output JSON file."
    )
    args = parser.parse_args()

    print(f"Generating schema from {args.input}...")
    data_g = generate_schema_graph(args.input)
    schema_json = extract_labels_and_placeholders(data_g)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        json.dump(schema_json, f, indent=4)

    print(f"Schema JSON written to {args.output}")
