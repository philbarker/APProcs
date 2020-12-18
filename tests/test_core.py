import pytest
from approcs import AP


@pytest.fixture(scope="module")
def default_AP():
    ap = AP("")
    return ap


@pytest.fixture(scope="module")
def easy_AP():
    ap = AP("tests/input/courseSchemaAP.csv")
    print(ap)
    return ap


def test_statement():
    st = AP.CSVTripleConstraint()
    assert st
    assert st.propertyID == ""
    assert st.propertyLabel == ""
    assert st.mandatory == False
    assert st.repeatable == False
    assert st.valueNodeType == ""
    assert st.valueConstraint == ""
    assert st.valueConstraintType == ""
    assert st.valueShape == ""
    assert st.note == ""


def test_init_default(default_AP):
    assert default_AP.metadata == {"author": "", "name": ""}
    assert default_AP.namespaces == {
        "dct": "http://purl.org/dc/terms/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "sdo": "https://schema.org/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
    }
    assert default_AP.headingMap.lookup("Note") == "note"
    assert default_AP.shapes["default"]
    assert default_AP.shapes["default"].shapeID == ""
    assert default_AP.shapes["default"].shapeClosed == ""
    assert default_AP.shapes["default"].start == False
    assert default_AP.shapes["default"].tc_list == []


def test_init(easy_AP):
    print(easy_AP.shapes.keys())
    print(easy_AP.shapes["CourseInstance"])
    expected_st0 = AP.CSVTripleConstraint(
        propertyID="rdf:type",
        propertyLabel="instance of",
        mandatory="y",
        repeatable="n",
        valueNodeType="IRI",
        valueDataType="",
        valueConstraint="sdo:CourseInstance",
        valueConstraintType="",
        valueShape="",
        note="",
    )
    assert easy_AP.metadata == {"author": "", "name": ""}
    for sh_id in ["CourseInstance", "Subject", "Location", "Instructor"]:
        assert sh_id in easy_AP.shapes.keys()
        assert easy_AP.shapes[sh_id].shapeID == sh_id
    assert easy_AP.shapes["CourseInstance"].shapeID == "CourseInstance"
    assert easy_AP.shapes["CourseInstance"].shapeLabel == "Course Offering"
    st0 = easy_AP.shapes["CourseInstance"].tc_list[0]
    for elem_id in [
        "propertyID",
        "propertyLabel",
        "mandatory",
        "repeatable",
        "valueNodeType",
        "valueDataType",
        "valueConstraint",
        "valueConstraintType",
        "valueShape",
        "note",
    ]:
        assert elem_id in vars(st0)
    assert st0 == expected_st0
