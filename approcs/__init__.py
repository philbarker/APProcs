import csv, yaml


class APProcs(dict):
    """ The a dict of the application profile, each value is a list of dicts, a list for each type containing dicts for each row of that type. Methods to read, display and process that AP.
    Keys of top level dict are hard coded:
        base       - a list of the AP base dict
        namespaces - a list of the namespace dicts
        entities   - a list of the entity dicts
        statements - a list of the statement dicts
    """

    def __init__(self, infile):
        """set the class properties to their types and optionally, if a csv  file is specified, read the data in"""
        self["base"] = list()
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
                if "base" == row["Type"].lower():
                    self["base"].append(row)
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

    def build_yama(self):
        """build a YAMA representation of the AP"""
        # idea is just to test that internal representation of AP is useful for something, otherwise could just store csv lines as found
        yama = dict()
        yama["YAMA"] = "1.0"
        yama["description_set"] = dict()
        yama["description_set"]["ID"] = self["base"][0]["ID"]
        yama["description_set"]["title"] = self["base"][0]["Label"]
        yama["description_set"]["entities"] = list()
        yama["namespaces"] = dict()
        for i in range(0, len(self["namespaces"])):
            k = self["namespaces"][i]["ID"]
            v = self["namespaces"][i]["Property"]
            yama["namespaces"][k] = v
        yama["descriptions"] = dict()
        for i in range(0, len(self["entities"])):
            e = self["entities"][i]
            yama["description_set"]["entities"].append(e["ID"])
            d = dict()
            d["maps_to"] = e["Property"]
            if ("y" == e["Mandatory"]):
                d["min"] = 1
            else:
                d["min"] = 0
            if ("y" == e["Repeatable"]):
                d["max"] = "unlimited"
            else:
                d["max"] = 1
            d["standalone"] = str()
            d["statements"] = list()
            d["label"] = e["Label"]
            d["annotation"] = e["Annotation"]
            yama["descriptions"][e["ID"]] = d
        yama["statements"] = dict()
        for i in range(0, len(self["statements"])):
            s = self["statements"][i]
            on_e = s["on entity"]
            yama["descriptions"][on_e]["statements"].append(s["ID"])
            d = dict()
            d["property"] = s["Property"]
            d["type"] = s["ValueType"]
            d["value"] = s["Value"]
            if ("y" == s["Mandatory"]):
                d["min"] = 1
            else:
                d["min"] = 0
            if ("y" == s["Repeatable"]):
                d["max"] = "unlimited"
            else:
                d["max"] = 1
            d["label"] = s["Label"]
            d["annotation"] = s["Annotation"]
            yama["statements"][s["ID"]] = d
        return yama
