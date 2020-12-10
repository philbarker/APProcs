import pytest
from approcs import AP


@pytest.fixture
def default_AP():
    ap = AP("")
    return ap


@pytest.fixture
def easy_AP():
    ap = AP("tests/input/courseSchemaAP.csv")
    return ap


def test_init_default(default_AP):
    assert default_AP["metadata"] == {"author": "", "name": ""}
    assert default_AP["namespaces"] == {
        "dct": "http://purl.org/dc/terms/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "sdo": "https://schema.org/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
    }
    assert default_AP["shapes"] == {
        "default": {
            "shapeClosed": False,
            "shapeLabel": "default shape",
            "termConstraints": [],
        }
    }
    assert default_AP["headingMap"].lookup("Note") == "note"


def test_init(easy_AP):
    assert easy_AP["metadata"] == {"author": "", "name": ""}
    for sh_id in ["CourseInstance", "Subject", "Location", "Instructor"]:
        assert sh_id in easy_AP["shapes"].keys()
    assert len(easy_AP["shapes"]["CourseInstance"]) == 3


#    assert easy_AP["shapes"]["CourseInstance"]["termConstraints"] == "fred"
#    for elem_id in ["inShape", "propertyID", "propertyLabel", "mandatory", "repeatable", "valueNodeType", "valueDataType","valueConstraint", "valueConstraintType", "valueShape", "note"]:
#        assert elem_id in easy_AP["shapes"]["CourseInstance"]["termConstraints"][0]
