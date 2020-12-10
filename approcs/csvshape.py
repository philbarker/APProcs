"""Classes for Python objects derived from CSV files."""


class CSVShape(dict):
    """A dict class for information about a shape and a list of term constraints for that shape."""

    def __init__(
        self,
        shapeLabel: str = "default shape",
        shapeClosed: bool = bool(),
        termConstraints: list = list(),
    ):
        super().__init__()
        self["shapeLabel"]: str = shapeLabel
        self["shapeClosed"]: bool = shapeClosed
        self["termConstraints"]: list = termConstraints

    def add_value(self, key: str, value):
        print(key, value, type(value))
        if key == "shapeLabel":
            if type(value) is str:
                self["shapeLabel"] = value
            else:
                print("value of shapeLabel must be a string")
        elif key == "shapeClosed":
            if type(value) is bool:
                self["shapeClosed"] = value
            else:
                print("value of shapeClosed must be a boolean")
        elif key == "termConstraints":
            if type(value) is CSVTripleConstraint:
                self["termConstraints"].append(value)
            else:
                print("value of termConstraints must be a CSVTripleConstraint")
        else:
            print("%s is not a known element for CSVShape" % key)


class CSVTripleConstraint(dict):
    """A dict class for key-value pairs that describe a triple constraint."""

    def __init__(self):
        super().__init__()
        self["inShape"] = str()
        self["propertyID"] = str()
        self["propertyLabel"] = str()
        self["mandatory"] = bool()
        self["repeatable"] = bool()
        self["valueNodeType"] = str()
        self["valueDataType"] = str()
        self["valueConstraint"] = list()
        self["valueConstraintType"] = str()
        self["valueShape"] = str()
        self["note"] = str()

    def add_value(self, key, value):
        if key == valueConstraint:
            self["valueConstraint"].add(value)
        elif key in self.keys():
            self[key] = value
        else:
            print("%s is not a known element for CSVTripleConstraint" % key)


class Namespaces(dict):
    """A dict class for namespaces, ns : uri"""

    # FIXME: need to be able to read in values
    # for now just run with some defaults
    def __init__(self):
        super().__init__()
        self["sdo"] = "https://schema.org/"
        self["dct"] = "http://purl.org/dc/terms/"
        self["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
        self["xsd"] = "http://www.w3.org/2001/XMLSchema#"


class Metadata(dict):
    """A dict class for information about an application profile"""

    # FIXME: need to be able to read in values
    # for now just run with some defaults
    def __init__(self):
        super().__init__()
        self["name"] = ""
        self["author"] = ""


class HeadingMap(dict):
    """Dict class for mapping TAP standard headings to custom values."""

    # FIXME: need to be able to read in values
    # for now just run with some defaults
    def __init__(self):
        super().__init__()
        self["shapeID"] = "shapeID"
        self["shapeLabel"] = "shapeLabel"
        self["propertyID"] = "propertyID"
        self["propertyLabel"] = "propertyLabel"
        self["mandatory"] = "mandatory"
        self["repeatable"] = "repeatable"
        self["valueNodeType"] = "valueNodeType"
        self["valueDatatype"] = "valueDatatype"
        self["valueShape"] = "valueShape"
        self["valueConstraint"] = "valueConstraint"
        self["valueConstraintType"] = "valueConstraintType"
        self["valueShape"] = "valueShape"
        self["note"] = "Note"

    def lookup(self, value):
        """given the heading from the table, find the standard TAP heading"""
        # Brute force lookup seems fastest, https://therenegadecoder.com/code/how-to-perform-a-reverse-dictionary-lookup-in-python/
        for tap_heading, custom_heading in self.items():
            if value == custom_heading:
                return tap_heading
        return "unknown"  # if value not found

    def invert(self):
        # better for getting a full set of reverse lookups
        return {value: key for key, value in self.items()}
