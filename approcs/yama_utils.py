from yaml import dump


def build_yama(ap):
    """build a YAMA representation of the AP"""
    # idea is just to test that internal representation of AP is useful for something, otherwise could just store csv lines as found
    yama = dict()
    yama["YAMA"] = "1.0"
    yama["description_set"] = dict()
    yama["description_set"]["ID"] = "not known"
    yama["description_set"]["title"] = "not known"
    yama["description_set"]["version"] = "not known"
    yama["description_set"]["date"] = None
    yama["description_set"]["subject"] = None
    yama["description_set"]["creator"] = None
    yama["description_set"]["open"] = None
    yama["description_set"]["license"] = None
    yama["description_set"]["descriptions"] = list()
    yama["namespaces"] = dict()
    for ns in ap["namespaces"].keys():
        yama["namespaces"][ns] = ap["namespaces"][ns]["URI"]
    yama["descriptions"] = dict()
    for s in ap["shapes_meta"].keys():  # Build metadata about shape
        if s == "None":
            continue  # key is for statements not about a shape
        meta = ap["shapes_meta"][s]
        yama["description_set"]["descriptions"].append(s)
        d = dict()
        d["label"] = meta["ID"]
        if meta["Label"]:
            d["name"] = meta["Label"]
        else:
            d["name"] = meta["ID"][1:]
        if meta["Comment"]:
            d["description"] = meta["Comment"]
        if "y" == meta["Mandatory"]:
            d["min"] = 1
        else:
            d["min"] = 0
        if "y" == meta["Repeatable"]:
            d["max"] = "unlimited"
        else:
            d["max"] = 1
        d["standalone"] = True
        d["statements"] = list()
        yama["descriptions"][s] = d
    yama["statements"] = dict()
    yama["constraints"] = dict()
    for shape in ap["shape_props"].keys():
        if shape == "None":
            continue  # key is for statements not about a shape
        # otherwise we have a list of statements about properties for a shape
        for statement in ap["shape_props"][shape]:
            # add to list of statements for relevant YAMA description
            yama["descriptions"][shape]["statements"].append(statement["ID"])
            # build a YAMA entry for the statement
            d = dict()
            d["label"] = statement["URI"]
            d["property"] = statement["URI"]
            if statement["Label"]:
                d["name"] = statement["Label"]
            else:
                d["name"] = statement["URI"]
            if "y" == statement["Mandatory"]:
                d["min"] = 1
            else:
                d["min"] = 0
            if "y" == statement["Repeatable"]:
                d["max"] = "unlimited"
            else:
                d["max"] = 1
            if statement["Comment"]:
                d["description"] = statement["Comment"]
            if statement["Type"] or statement["Value Space"]:
                cID = "c" + statement["ID"]
                d["constraints"] = cID
                yama["constraints"][cID] = build_constraint(
                    statement["Type"], statement["Value Space"]
                )
            yama["statements"][statement["ID"]] = d
    return yama


def build_constraint(value_type, value_space):
    constraint = dict()
    constraint["type"] = "not done"
    constraint["notes"] = "somthing to do with %s and %s." % (value_type, value_space)
    return constraint


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


def dump_yama(yama):
    print(dump(yama, default_flow_style=False))
