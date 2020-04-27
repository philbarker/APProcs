import yaml

def build_yama(ap):
    """build a YAMA representation of the AP"""
    # idea is just to test that internal representation of AP is useful for something, otherwise could just store csv lines as found
    yama = dict()
    yama["YAMA"] = "1.0"
    yama["description_set"] = dict()
    yama["description_set"]["ID"] = ap["base"][0]["ID"]
    yama["description_set"]["title"] = ap["base"][0]["Label"]
    yama["description_set"]["entities"] = list()
    yama["namespaces"] = dict()
    for i in range(0, len(ap["namespaces"])):
        k = ap["namespaces"][i]["ID"]
        v = ap["namespaces"][i]["Property"]
        yama["namespaces"][k] = v
    yama["descriptions"] = dict()
    for i in range(0, len(ap["entities"])):
        e = ap["entities"][i]
        yama["description_set"]["entities"].append(e["ID"])
        d = dict()
        d["maps_to"] = e["Property"]
        if "y" == e["Mandatory"]:
            d["min"] = 1
        else:
            d["min"] = 0
        if "y" == e["Repeatable"]:
            d["max"] = "unlimited"
        else:
            d["max"] = 1
        d["standalone"] = str()
        d["statements"] = list()
        d["label"] = e["Label"]
        d["annotation"] = e["Annotation"]
        yama["descriptions"][e["ID"]] = d
    yama["statements"] = dict()
    for i in range(0, len(ap["statements"])):
        s = ap["statements"][i]
        on_e = s["on entity"]
        yama["descriptions"][on_e]["statements"].append(s["ID"])
        d = dict()
        d["property"] = s["Property"]
        d["type"] = s["ValueType"]
        d["value"] = s["Value"]
        if "y" == s["Mandatory"]:
            d["min"] = 1
        else:
            d["min"] = 0
        if "y" == s["Repeatable"]:
            d["max"] = "unlimited"
        else:
            d["max"] = 1
        d["label"] = s["Label"]
        d["annotation"] = s["Annotation"]
        yama["statements"][s["ID"]] = d
    return yama
