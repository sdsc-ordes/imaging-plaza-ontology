from pyshacl import validate
import rdflib
import sys

def run_shacl_validation(data_file, shapes_file):
    try:
        # Load the data graph
        data_graph = rdflib.Graph()
        data_graph.parse(data_file, format="turtle")
        print(f"Data graph loaded with {len(data_graph)} triples.")

        # Load the SHACL shapes graph
        shapes_graph = rdflib.Graph()
        shapes_graph.parse(shapes_file, format="turtle")
        print(f"Shapes graph loaded with {len(shapes_graph)} triples.")

        # Perform SHACL validation
        conforms, results_graph, results_text = validate(
            data_graph=data_graph,
            shacl_graph=shapes_graph,
            inference='rdfs',
            debug=False
        )
        print("Validation Results:")
        print(results_text)
        if conforms:
            print("The ontology conforms to the shacl-shacl shapes.")
        else:
            print("The ontology does not conform to the shacl-shacl shapes.")
        return conforms
    except Exception as e:
        print(f"An error occurred during SHACL validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    data_file = "build/ontology_combined.ttl"
    shapes_file = "src/quality-checks/shacl-shacl.ttl"

    print(f"Running SHACL validation on {data_file} with shapes {shapes_file}...")
    conforms = run_shacl_validation(data_file, shapes_file)
    sys.exit(0 if conforms else 1)