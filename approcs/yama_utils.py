from yaml import dump


def build_yama(self):
    """build a YAMA representation of the AP"""
    # idea is just to test that internal representation of AP is useful for something, otherwise could just store csv lines as found
    ap = self
    yama = dict()
    yama["YAMA"] = "1.0"
    yama["description_set"] = dict()
    yama["description_set"]["ID"] = "can't generate"
    yama["description_set"]["title"] = "can't generate"
    yama["description_set"]["entities"] = list()
    yama["namespaces"] = dict()
    for ns in ap["namespaces"].keys():
        yama["namespaces"][ns] = ap["namespaces"][ns]["URI"]
    yama["descriptions"] = dict()
    for s in ap["shapes_meta"].keys(): #Build metadata about shape
        if (s == "All"): continue # All key is for statements not about a shape
        meta = ap["shapes_meta"][s]
        yama["description_set"]["entities"].append(s)
        d = dict()
        d["maps_to"] = find_type_mapping(ap["namespaces"], ap["shape_props"][s])
        if "y" == meta["Mandatory"]:
            d["min"] = 1
        else:
            d["min"] = 0
        if "y" == meta["Repeatable"]:
            d["max"] = "unlimited"
        else:
            d["max"] = 1
        d["standalone"] = str()
        d["statements"] = list()
        d["label"] = meta["Label"]
        d["annotation"] = meta["Comment"]
        yama["descriptions"][meta["ID"]] = d
    yama["statements"] = dict()
    for e in ap["shape_props"].keys():
        if (e == "All"): continue # All key is for statements not about a shape
        for s in ap["shape_props"][e]:
            yama["descriptions"][e]["statements"].append(s["ID"])
            d = dict()
            d["property"] = s["URI"]
            d["type"] = s["Type"]
            d["value"] = s["Value Space"]
            if "y" == s["Mandatory"]:
                d["min"] = 1
            else:
                d["min"] = 0
            if "y" == s["Repeatable"]:
                d["max"] = "unlimited"
            else:
                d["max"] = 1
            d["label"] = s["Label"]
            d["annotation"] = s["Comment"]
            yama["statements"][s["ID"]] = d
    return yama


def find_type_mapping(namespaces, statements):
    """given the statementa about one shape, as a list of dicts, returns URIs specified as required values for rdf:type property"""
    # find ns for rdf
    rdfUri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    for ns in namespaces.keys():
        if namespaces[ns]["URI"] == rdfUri:
            rdfNS = ns
            break
    # look for statement constraining rdf:type
    for s in statements:
        if (s["URI"] == rdfNS + ":type") or (s["URI"] == rdfUri + "type"):
            return s["Value Space"].split(" ")
    # if no rdf:type found call it a rdfs:Resource
    # FIXME: check consequences of this
    return "http://www.w3.org/2000/01/rdf-schema#Resource"


def dump_yama(self, yama):
    print(dump(yama, default_flow_style=False))
