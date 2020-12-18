import pprint
from csv2shex import csvreader
from dataclasses import asdict
class AP:
    from csv2shex import CSVTripleConstraint, CSVShape
    from .shape_info import Namespaces, Metadata, HeadingMap

    """ The application profile data and methods to read & display.
    Comprises dicts for:
        namespaces  - a dict of namespaces prefix: URI pairs
        metadata - a dict of statements about the application profile
        shapes - a dict for elements about shapes
    """

    def __init__(self, infile):
        """set the class properties to their types and optionally, if a csv  file is specified, read the data in"""
        self.namespaces = self.Namespaces()
        self.metadata = self.Metadata()
        self.shapes = dict(default=self.CSVShape())
        self.headingMap = self.HeadingMap()
        if infile:
            shape_list = csvreader(infile)
            for sh in shape_list:
                self.shapes[sh.shapeID] = sh
        else:
            print("no input file specified")
        return

    def dump(self):
        """print key: value pairs for all dicts of type(s) t; if t is empty print all"""
        pp = pprint.PrettyPrinter(indent=2)
        print("\n\n=== Namespaces ===")
        pp.pprint(self.namespaces)
        print("\n\n=== Metadata ===")
        pp.pprint(self.metadata)
        print("\n\n=== Heading Map ===")
        pp.pprint(self.headingMap)
        print("\n\n=== Shapes ===")
        for sh_id in self.shapes.keys() :
            print(sh_id)
            sh_dict = asdict(self.shapes[sh_id])
            pp.pprint(sh_dict)


#        for entry in self.keys():
#            print("\n\n=== " + entry + " ===")
#            pp.pprint(self[entry])
#        return True
