# Imaging Plaza Ontology

This repo contains the SHACL shapes and the IP Ontology used for: 

- Fair Calculation

## Basic Schema Diagram (UML)

![ontology_combined](https://github.com/user-attachments/assets/6b8cafae-9e2c-4dbc-a3e0-f1915f343d81)

## Changelog

- **v0.1**: Initial release, ex: prefixes updated, sh:nodekind sh:IRI replaced with a regex.
- **v0.2**: Changed shapes, ontology definitions, fairlevel validator.
- **v0.3**: Changed fair calculation.
- **v0.4**: Fixed loose nodes for PySHACL.
- **v0.5**: Updated definitions, cardinality of several shapes.
- **v0.6**: Added ontology metadata.
- **v0.7**: Internalize & objectify hasExecutableNotebook, update prefixes from ex: to imag:
- **v0.8**: Update FAIR levels, contributors+producers become authors. First+Last name becomes schema:name.
- **v0.9**: Support for runnable examples, dicom dataset properties, spelling mistakes.
- **v1.0**: Update enumerations modelling to use skos for taxonomy, expand meta-shacl shapes, Various CI improvements, removal of unused properties and shapes.

