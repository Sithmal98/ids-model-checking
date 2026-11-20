# IDS Specifications and Model Checking

Python scripts that use IfcTester (part of IfcOpenShell) to write Information Delivery Specification (IDS) files and check IFC models against them. Made for the openBIM data structures exercise in my MSc Digital Civil Engineering Science (TU Wien).

## What it does

**Part 1: Author an IDS file**

A script that creates an IDS file with these rules:
- Entity: the model must not contain a column
- Property: the number of risers of a stair must be less than 22, and every door must have a fire rating from an allowed list
- Material: elements made of timber must not be combustible
- Attribute: all door names follow the pattern Door-001, Door-002, ...
- Part of: every wall, slab, door, window, stair, railing and column belongs to a building storey
- Classification: every slab is classified as "Slab construction" in the CCI, referring to the buildingSMART Data Dictionary

**Part 2: Validate an IFC model**

A script that checks an IFC model against the IDS file and prints the report to the console.

**Part 3: Correct a given IDS file**

Reviewed an IDS file with errors, found illogical specifications, structural errors and IFC schema errors, and corrected them.

## Tools

Python, IfcOpenShell, IfcTester, IDS

## How to run

    pip install ifcopenshell
    python create_ids.py
    python validate_ifc.py
