import csv


class APProcs(dict):
    """ The a dict of the application profile, each value is a list of dicts, a list for each type containing dicts for each row of that type. Methods to read, display and process that AP.
    Keys of top level dict are hard coded:
        namespaces - a list of the namespace dicts
        entities   - a list of the entity dicts
        statements - a list of the statement dicts
    """

    import yaml
    from .yama_utils import build_yama
    from .rdfs_utils import make_base_graph, make_ap_graph

    def __init__(self, infile):
        """set the class properties to their types and optionally, if a csv  file is specified, read the data in"""
        self["namespaces"] = list()
        self["entities"] = list()
        self["statements"] = list()
        if infile:
            self.read_input(infile)
        else:
            print("no input file specified")
        return

    def read_input(self, infile):
        """read a csv into list of dicts, one for each row in csv except for first row which is used as keys."""
        with open(infile) as csvfile:
            apreader = csv.DictReader(csvfile)
            last_entity = ""
            last_type = ""
            success = True
            for row in apreader:
                if row["Type"]:
                    last_type = row["Type"]
                else:
                    row["Type"] = last_type
                elif "prefix" == row["Type"].lower():
                    self["namespaces"].append(row)
                elif "entity" == row["Type"].lower():
                    last_entity = row["ID"]
                    self["entities"].append(row)
                elif "statement" == row["Type"].lower():
                    row["on entity"] = last_entity
                    self["statements"].append(row)
                else:
                    print("Warning could not proces row type " + row["Type"])
                    success = False
        return success

    def dump(self, t=""):
        """print key: value pairs for all dicts of type t; if t is empty print all"""
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
                for r in self[atype]:
                    for key in r.keys():
                        print(key + ", " + r[key])
                    print("-----")
            else:
                print("cannot print info for unknown type " + atype)
        return True
