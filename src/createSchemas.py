import rdflib
import requests
import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, QueryResult, TURTLE, CSV, JSONLD
import pyshacl
import json 


def generate_schema_json(turtle_file: str) -> dict:
    """
    Generate schema JSON from rdflib.Graph.

    Args:
        data_g: The rdflib.Graph object containing the data.

    Returns:
        The schema as a dictionary.
    """
    data_g = rdflib.Graph()
    data_g.parse(turtle_file, format="turtle")
    
    return data_g

data_g = generate_schema_json("schemas/ImagingOntology.ttl")

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
        "general_table_action": "Action"
    }
    for row in result:
        iri = str(row.iri)
        slug = iri.split('/')[-1].split('#')[-1]
        if row.label:
            schema_json[f"{slug}_label"] = str(row.label)
        if row.comment:
            schema_json[f"{slug}_placeholder"] = str(row.comment)
    return schema_json

schema_json = extract_labels_and_placeholders(data_g)

with open("locales/en/schema.json", "w") as f:
    json.dump(schema_json, f, indent=4)