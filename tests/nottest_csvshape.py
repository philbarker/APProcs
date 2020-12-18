import pytest
from approcs.csvshape import (
    CSVTripleConstraint,
    CSVShape,
    Namespaces,
    Metadata,
    HeadingMap,
)


default_shape_dict = {
    "shapeClosed": False,
    "shapeLabel": "default shape",
    "termConstraints": [],
}
default_constraint_dict = {
    "inShape": "",
    "propertyID": "",
    "propertyLabel": "",
    "mandatory": False,
    "repeatable": False,
    "valueNodeType": "",
    "valueDataType": "",
    "valueConstraint": [],
    "valueConstraintType": "",
    "valueShape": "",
    "note": "",
}


def test_shape_init():
    sh = CSVShape()
    print(sh)
    assert sh == default_shape_dict


def test_constraint_init():
    tc = CSVTripleConstraint()
    assert tc == default_constraint_dict


def test_shape_add_value():
    sh = CSVShape()
    tc = CSVTripleConstraint()
    sh.add_value("shapeClosed", True)
    assert sh["shapeClosed"]
    sh.add_value("shapeLabel", "new label")
    assert sh["shapeLabel"] == "new label"
    sh.add_value("termConstraints", tc)
    assert sh["termConstraints"][0] == default_constraint_dict
