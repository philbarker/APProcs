import csv, pprint
from .csvshape import CSVTripleConstraint, CSVShape, Namespaces, Metadata, HeadingMap


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
        self["shapes"] = dict(default=CSVShape())
        self["headingMap"] = HeadingMap()
        if infile:
            self.read_input(infile)
        else:
            print("no input file specified")
        return

    def isEmptyRow(self, dictionary):
        for key in dictionary:
            if dictionary[key]:
                return False
        return True

    def read_input(self, infile):
        """read a csv into AP["shapes"], one for each row in csv except for first row which is used as keys."""

        mapped_headings = self["headingMap"].invert()
        shape_id_heading = mapped_headings["shapeID"]
        property_id_heading = mapped_headings["propertyID"]
        with open(infile) as csvfile:
            apreader = csv.DictReader(csvfile)
            current_shape = CSVShape()
            current_shape_ID = "default"
            c = int(0)
            for row in apreader:
                if self.isEmptyRow(row):
                    # ignore empty rows; next please
                    continue
                if row[property_id_heading]:
                    # row has elements about a property
                    p_Elements = CSVTripleConstraint()
                    for r_heading in row.keys():
                        tap_elem = mapped_headings[r_heading]
                        p_Elements[tap_elem] = row[r_heading]
                    current_shape.add_value("termConstraints", p_Elements)
                if row[shape_id_heading]:
                    # There's shape information
                    if row[shape_id_heading] != current_shape_ID:
                        # FIXME: is assuming this shapeID hasn't been used before
                        # save current shape and start a new one
                        self["shapes"][current_shape_ID] = current_shape
                        current_shape = CSVShape()
                        current_shape_ID = row[shape_id_heading]
                        current_shape["shapeLabel"] = row[mapped_headings["shapeLabel"]]
                # save the last shape
                # (others were saved when new ones were needed)
                self["shapes"][current_shape_ID] = current_shape
        return

    def dump(self):
        """print key: value pairs for all dicts of type(s) t; if t is empty print all"""
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self)

        for entry in self.keys():
            print("\n\n=== " + entry + " ===")
            pp.pprint(self[entry])
        return True
