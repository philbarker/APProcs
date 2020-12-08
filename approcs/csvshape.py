"""Classes for Python objects derived from CSV files."""

class CSVShape(dict):
    """A dict class for information about a shape and a list of term constraints for that shape."""
    def __init__(self, shapeLabel:str = "default shape", shapeClosed:bool = bool(), termConstraints:list = list()):
        super().__init__()
        self["shapeLabel"]:str = shapeLabel
        self["shapeClosed"]:bool = shapeClosed
        self["termConstraints"]:list = termConstraints

    def add_value(self, key:str, value):
        if key == shapeLabel or shapeClosed:
            if type(self[key]) == "str" :
                self[key] = value
                print("value of %s must be a string" % key)
        elif key == termConstraints:
            if type(self[key]) == "CSVTripleConstraint":
                self["termConstraints"].add(value)
            else:
                print("value of %s must be a CSVTripleConstraint" %  key)
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
    def __init__(self):
        super().__init__()
        self["sdo"]  = "https://schema.org/"
        self["dct"]  = "http://purl.org/dc/terms/"
        self["rdf"]  = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
        self["xsd"]  = "http://www.w3.org/2001/XMLSchema#"

class Metadata(dict):
    """A dict class for information about an application profile"""
    def __init__(self):
        self["name"]  = ""
        self["author"]  = ""
