import json
import ifcopenshell

from ifctester import ids
from ifctester import reporter


IFC_FILE = "CustomTestModel-BIM-Datastructure-Exercise.ifc"

BROKEN_IDS_FILE = "BIM-Data-Structure-IDS-Exercise-Group 2.ids"

CREATED_IDS_FILE = "01_Group2_Created_IDS.ids"

VALIDATION_TXT = "02_Group2_Validation_Report.txt"
VALIDATION_JSON = "02_Group2_Validation_Report.json"

CORRECTED_IDS_FILE = "03_Group2_Corrected_IDS.ids"
CORRECTION_NOTES = "03_Group2_Correction_Notes.txt"

def create_ids():

    my_ids = ids.Ids(
        title="IDS Exercise Solution",
        version="1.0",
        description="IDS created with IfcTester"
    )

    spec = ids.Specification(
        name="No IfcColumn allowed",
        minOccurs=0,
        maxOccurs=0,
        ifcVersion=["IFC4"]
    )

    spec.applicability.append(
        ids.Entity(name="IFCCOLUMN")
    )

    my_ids.specifications.append(spec)

    spec = ids.Specification(
        name="Stair NumberOfRiser < 22",
        ifcVersion=["IFC4"]
    )

    spec.applicability.append(
        ids.Entity(name="IFCSTAIR")
    )

    spec.requirements.append(
        ids.Property(
            propertySet="Pset_StairCommon",
            baseName="NumberOfRiser",
            value=ids.Restriction(
                options={"maxExclusive": 22},
                base="decimal"
            ),
            cardinality="required"
        )
    )

    my_ids.specifications.append(spec)

    spec = ids.Specification(
        name="Door Fire Rating",
        ifcVersion=["IFC4"]
    )

    spec.applicability.append(
        ids.Entity(name="IFCDOOR")
    )

    spec.requirements.append(
        ids.Property(
            propertySet="Pset_DoorCommon",
            baseName="FireRating",
            value=ids.Restriction(
                options={
                    "enumeration": [
                        "EI2 30-C-S200",
                        "EI2 30"
                    ]
                },
                base="string"
            ),
            cardinality="required"
        )
    )

    my_ids.specifications.append(spec)

    spec = ids.Specification(
        name="Timber not combustible",
        ifcVersion=["IFC4"]
    )

    spec.applicability.append(
        ids.Material(
            value=ids.Restriction(
                options={"pattern": ".*[Tt]imber.*"},
                base="string"
            )
        )
    )

    spec.requirements.append(
        ids.Property(
            propertySet="Pset_MaterialCombustion",
            baseName="Combustible",
            value=False,
            dataType="IFCBOOLEAN",
            cardinality="required"
        )
    )

    my_ids.specifications.append(spec)

    spec = ids.Specification(
        name="Door naming convention",
        ifcVersion=["IFC4"]
    )

    spec.applicability.append(
        ids.Entity(name="IFCDOOR")
    )

    spec.requirements.append(
        ids.Attribute(
            name="Name",
            value=ids.Restriction(
                options={
                    "pattern": "^Door-[0-9]{3}$"
                },
                base="string"
            ),
            cardinality="required"
        )
    )

    my_ids.specifications.append(spec)

    entities = [
        "IFCWALL",
        "IFCSLAB",
        "IFCDOOR",
        "IFCWINDOW",
        "IFCSTAIR",
        "IFCRAILING",
        "IFCCOLUMN"
    ]

    for entity in entities:

        spec = ids.Specification(
            name=f"{entity} contained in storey",
            ifcVersion=["IFC4"]
        )

        spec.applicability.append(
            ids.Entity(name=entity)
        )

        spec.requirements.append(
            ids.PartOf(
                name="IFCBUILDINGSTOREY",
                relation="IFCRELCONTAINEDINSPATIALSTRUCTURE",
                cardinality="required"
            )
        )

        my_ids.specifications.append(spec)

    spec = ids.Specification(
        name="CCI Slab Construction",
        ifcVersion=["IFC4"]
    )

    spec.applicability.append(
        ids.Entity(name="IFCSLAB")
    )

    spec.requirements.append(
        ids.Classification(
            system="CCI",
            value="Slab construction",
            cardinality="required"
        )
    )

    my_ids.specifications.append(spec)

    my_ids.to_xml(CREATED_IDS_FILE)

    print(f"IDS file created: {CREATED_IDS_FILE}")

    return my_ids


def validate_ifc():

    model = ifcopenshell.open(IFC_FILE)

    my_ids = ids.open(CREATED_IDS_FILE)

    my_ids.validate(model)

    txt_report = reporter.Txt(my_ids)
    txt_report.report()
    txt_report.to_file(VALIDATION_TXT)

    json_report = reporter.Json(my_ids)

    with open(
        VALIDATION_JSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            json_report.report(),
            f,
            indent=4,
            default=str
        )

    print("\nVALIDATION RESULTS")
    print("=" * 60)
    print(txt_report.text)
    print("=" * 60)

def correct_given_ids():

    notes = []

    try:

        ids.open(BROKEN_IDS_FILE)

        notes.append(
            "Given IDS can be opened but contains logical errors."
        )

    except Exception as e:

        notes.append(
            "Given IDS contains structural/schema errors."
        )

        notes.append(str(e))

    corrected = ids.Ids(
        title="Corrected IDS",
        version="1.0",
        description="Corrected version of provided IDS"
    )

    spec = ids.Specification(
        name="Concrete Wall-001 load-bearing"
    )

    spec.applicability.append(
        ids.Entity(name="IFCWALL")
    )

    spec.applicability.append(
        ids.Attribute(
            name="Name",
            value="Wall-001"
        )
    )

    spec.applicability.append(
        ids.Material(
            value="Concrete"
        )
    )

    spec.requirements.append(
        ids.Property(
            propertySet="Pset_WallCommon",
            baseName="LoadBearing",
            value=True,
            dataType="IFCBOOLEAN",
            cardinality="required"
        )
    )

    corrected.specifications.append(spec)

    spec = ids.Specification(
        name="IfcSlab properties"
    )

    spec.applicability.append(
        ids.Entity(name="IFCSLAB")
    )

    spec.requirements.append(
        ids.Property(
            propertySet="Pset_SlabCommon",
            baseName="LoadBearing",
            dataType="IFCBOOLEAN",
            cardinality="required"
        )
    )

    corrected.specifications.append(spec)

    spec = ids.Specification(
        name="Wall-001 timber wall"
    )

    spec.applicability.append(
        ids.Entity(name="IFCWALL")
    )

    spec.applicability.append(
        ids.Attribute(
            name="Name",
            value="Wall-001"
        )
    )

    spec.requirements.append(
        ids.Material(
            value="Timber",
            cardinality="required"
        )
    )

    corrected.specifications.append(spec)

    spec = ids.Specification(
        name="External walls"
    )

    spec.applicability.append(
        ids.Entity(name="IFCWALL")
    )

    spec.applicability.append(
        ids.Property(
            propertySet="Pset_WallCommon",
            baseName="IsExternal",
            value=True,
            dataType="IFCBOOLEAN"
        )
    )

    spec.requirements.append(
        ids.Property(
            propertySet="Pset_WallCommon",
            baseName="LoadBearing",
            dataType="IFCBOOLEAN",
            cardinality="required"
        )
    )

    corrected.specifications.append(spec)

    spec = ids.Specification(
    name="Wall storey containment"
    )

    spec.applicability.append(
        ids.Entity(name="IFCWALL")
    )

    spec.requirements.append(
        ids.PartOf(
            name="IFCBUILDINGSTOREY",
            relation="IFCRELCONTAINEDINSPATIALSTRUCTURE",
            cardinality="required"
        )
    )

    corrected.specifications.append(spec)

    corrected.to_xml(CORRECTED_IDS_FILE)

    notes.extend([
        "",
        "Corrections performed:",
        "",
        "1. SLAB -> IFCSLAB",
        "2. Wrong datatypes corrected",
        "3. Applicability and requirements separated",
        "4. Logical contradictions removed",
        "5. IFCRELCONNECTSELEMENTS replaced by IFCRELCONTAINEDINSPATIALSTRUCTURE",
        "6. IFCBUILDING replaced by IFCBUILDINGSTOREY"
    ])

    with open(
        CORRECTION_NOTES,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("\n".join(notes))

    print(f"Corrected IDS saved: {CORRECTED_IDS_FILE}")
    print(f"Notes saved: {CORRECTION_NOTES}")

if __name__ == "__main__":

    print("\nPART 1 - CREATE IDS")
    create_ids()

    print("\nPART 2 - VALIDATE IFC")
    validate_ifc()

    print("\nPART 3 - CORRECT IDS")
    correct_given_ids()

    print("\nIDS Exercise completed.")

