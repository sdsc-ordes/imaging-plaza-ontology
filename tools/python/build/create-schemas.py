import rdflib
import json

import os



def generate_schema_graph(turtle_file: str) -> rdflib.Graph:
    """
    Generate rdflib.Graph from a Turtle file.

    Args:
        turtle_file: The path to the Turtle file.

    Returns:
        The rdflib.Graph object containing the data.
    """
    DATA_G = rdflib.Graph()
    DATA_G.parse(turtle_file, format="turtle")

    return DATA_G




def extract_labels_and_placeholders(DATA_G: rdflib.Graph) -> dict:
    """
    Extract labels and placeholders from rdflib.Graph.

    Args:
        DATA_G: The rdflib.Graph object containing the data.

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
    result = DATA_G.query(query)
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

DATA_G = generate_schema_graph(str(os.getcwd()) + "/src/imaging-ontology/ImagingOntologyCombined.ttl" )

schema_json = extract_labels_and_placeholders(DATA_G)
os.makedirs(str(os.getcwd()) + "/build/locales/en", exist_ok=True)
with open(str(os.getcwd()) + "/build/locales/en/schema.json", "w") as f:
    json.dump(schema_json, f, indent=4)
