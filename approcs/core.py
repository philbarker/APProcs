import csv, pprint


class AP(dict):
    """ A dict of the application profile and methods to read, display and process that AP.
    Keys of top level dict are hard coded:
        namespaces  - a dict of statemants about namespaces
        shapes_meta - a dict of statements about shapes
        shape_props - a dict of lists of statements about properties for each shape
    statements within each dict are themselves dicts of column_heading: cell value pairs from the rows in the csv.
    """

    def __init__(self, infile):
        """set the class properties to their types and optionally, if a csv  file is specified, read the data in"""
        super().__init__()
        self["namespaces"] = dict()
        self["shapes_meta"] = dict()
        self["shape_props"] = dict()
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
        """read a csv into list of dicts, one for each row in csv except for first row which is used as keys."""
        with open(infile) as csvfile:
            apreader = csv.DictReader(csvfile)
            current_shape = "None"
            self["shapes_meta"]["None"] = dict()
            self["shape_props"]["None"] = list()
            c = int(0)
            for row in apreader:
                c += 1
                #                print('reading line', c)
                if self.isEmptyRow(row):
                    # ignore empty rows; next please
                    continue
                if row["ID"] and row["ID"][-1] == ":":
                    # it's a namespace id
                    self["namespaces"][row["ID"][:-1]] = row
                elif row["ID"] and row["ID"][0] == "@":
                    # it's a shape id
                    current_shape = row["ID"]
                    self["shapes_meta"][current_shape] = row
                    self["shape_props"][current_shape] = list()
                else:  # statement constrains a property
                    row["ID"] = str(c)
                    self["shape_props"][current_shape].append(row)

        return

    def dump(self, t=""):
        """print key: value pairs for all dicts of type(s) t; if t is empty print all"""
        pp = pprint.PrettyPrinter(indent=4)
        if "" == t:
            types = self.keys()
        elif type(t) is str:
            types = [t]
        elif type(t) is list:
            types = t
        else:
            print("types to print must be list or string" + t)
            return False
        for atype in types:
            if atype in self.keys():
                print("\n\n=== " + atype + " ===")
                pp.pprint(self[atype])
            else:
                print("cannot print info for unknown type " + atype)
        return True
