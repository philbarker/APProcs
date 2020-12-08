import csv, pprint
from .csvshape import CSVTripleConstraint, CSVShape, Namespaces, Metadata

class AP(dict):
    """ The application profile data and methods to read & display.
    Comprises dicts for:
        namespaces  - a dict of namespaces prefix: URI pairs
        metadata - a dict of statements about the application profile
        shapes - a dict for elements about shapes
    """

    def __init__(self, infile):
        """set the class properties to their types and optionally, if a csv  file is specified, read the data in"""
        super().__init__()
        self["namespaces"] = Namespaces()
        self["metadata"] = Metadata()
        self["shapes"] = dict(default = CSVShape())
        self.__headingMap = self.set_headingMap()
        if infile:
            self.read_input(infile)
        else:
            print("no input file specified")
        return

    def set_headingMap(self):
        #FIXME: read from file
        #This is default
        headingMap = {
            "shapeID":"shapeID",
            "shapeLabel":"shapeLabel",
            "propertyID":"propertyID",
            "propertyLabel":"propertyLabel",
            "mandatory":"mandatory",
            "repeatable":"repeatable",
            "valueNodeType":"valueNodeType",
            "valueDatatype":"valueDatatype",
            "valueShape":"valueShape",
            "valueConstraint":"valueConstraint",
            "valueConstraintType":"valueConstraintType",
            "valueShape":"valueShape",
            "note":"Note"
        }
        return headingMap

    def isEmptyRow(self, dictionary):
        for key in dictionary:
            if dictionary[key]:
                return False
        return True

    def read_input(self, infile):
        """read a csv into list of dicts, one for each row in csv except for first row which is used as keys."""
        #local vars for column headers
        headingMap = self.headingMap
        shapeID = headingMap["shapeID"]
        shapeLabel = headingMap["shapeLabel"]
        propertyID = headingMap["propertyID"]
        propertyLabel = headingMap["propertyLabel"]
        mandatory = headingMap["mandatory"]
        repeatable = headingMap["repeatable"]
        valueNodeType = headingMap["valueNodeType"]
        valueDatatype = headingMap["valueDatatype"]
        valueShape = headingMap["valueShape"]
        valueConstraint = headingMap["valueConstraint"]
        valueConstraintType = headingMap["valueConstraintType"]
        valueShape = headingMap["valueShape"]
        note = headingMap["note"]

        with open(infile) as csvfile:
            apreader = csv.DictReader(csvfile)
            current_shape = CSVShape()
            c = int(0)
            for row in apreader:
                if self.isEmptyRow(row):
                # ignore empty rows; next please
                    continue
                if row["propertyID"] :
                # row has elements about a property
                # FIXME needs to cope with missing columns
                    p_Elements = CSVTripleConstraint()
                    p_Elements.propertyID = row[propertyID]
                    p_Elements.propertyLabel = row[propertyLabel]
                    p_Elements.mandatory = row[mandatory]
                    p_Elements.repeatable = row[repeatable]
                    p_Elements.valueNodeType = row[valueNodeType]
                    p_Elements.valueDatatype = row[valueDatatype]
                    p_Elements.valueConstraint = row[valueConstraint]
#                    p_Elements.valueConstraintType = row[valueConstraintType]
                    p_Elements.valueShape = row[valueShape]
                    current_shape.tripleconstraints_list.append(p_Elements)
                if row["shapeID"] :
                # There's shape information
                    if row[shapeID] !=  current_shape.shapeID :
                    # FIXME assuming this shapeID hasn't been used before
                    # save current shape start a new one
                        self.shapes[current_shape.shapeID] = current_shape
                        current_shape = CSVShape()
                        current_shape.shapeID = row[shapeID]
                        current_shape.shapeLabel = row[shapeLabel]
                # this is the last shape being saved;
                # other shapes are saved as new shapes are needed
                self.shapes[current_shape.shapeID] = current_shape
        return

    def dump(self):
        """print the application profile"""
        pp = pprint.PrettyPrinter(indent=4)
        print("\n\n=== " + "Namespaces" + " ===")
        pp.pprint(self.namespaces)
        print("\n\n=== " + "Metadata" + " ===")
        pp.pprint(self.metadata)
        print("\n\n=== " + "Shapes" + " ===")
        pp.pprint(self.shapes)

        return True
