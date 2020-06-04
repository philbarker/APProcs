import json, pprint


class ShexAP:
    """the application profile in ShEx with some utility methods
       properties:
       - shex_j : a python dict equivalent of the shex json representation
       - namespaces : a dict of the namespaces in the AP
       methods:
       - create_j() creates the shex_j property
       - create_namespaces() creates the namespaces property
       - dump_j() prints the shex json representation of the AP
    """

    def __init__(self, ap=None):
        self.namespaces = dict()
        self.shex_j = dict()
        if ap:
            self.create_namespaces(ap)
        if ap:
            self.create_j(ap)
        return

    def create_namespaces(self, ap):
        # need to make a namespace for the shex instance b/c ap doesn't have one
        self.namespaces["shape_ns"] = "http://example.org/shapes#"
        for ns_id in ap["namespaces"].keys():
            self.namespaces[ns_id] = ap["namespaces"][ns_id]["URI"]

    def create_j(self, ap):
        self.shex_j = {
            "@context": "http://www.w3.org/ns/shex.jsonld",
            "type": "Schema",
            "shapes": list(),
        }
        for shape_id in ap["shapes_meta"].keys():
            if shape_id == "None":
                continue  # global node constraint, not a shape
                # to do: add global constraints
            shape_meta = ap["shapes_meta"][shape_id]
            shape_uri = self.namespaces["shape_ns"] + shape_meta["ID"][1:]
            prop_statements = ap["shape_props"][shape_id]
            self.add_shape(shape_uri, shape_meta, prop_statements)

    def add_shape(self, shape_uri, shape_meta, prop_statements):
        shape_d = dict()
        shape_d["id"] = shape_uri
        shape_d["type"] = "Shape"
        shape_d["expression"] = dict()
        shape_d["expression"]["type"] = "EachOf"
        shape_d["expression"]["expressions"] = list()
        for ps in prop_statements:
            shape_d["expression"]["expressions"].append(self.translate(ps))
        self.shex_j["shapes"].append(shape_d)
        return

    def translate(self, ps):
        """turn a statement about a property from the AP into a dict for a shex triple constraint"""
        constr_d = dict()
        constr_d["type"] = "TripleConstraint"
        constr_d["predicate"] = self.expand_ns(ps["URI"])
        if ps["Mandatory"]:
            # work out what we can for min triples for this property
            # AP has no min other than zero or one
            if ps["Mandatory"].lower() == "y":
                constr_d["min"] = 1
            else:
                constr_d["min"] = 0
        if ps["Repeatable"]:
            # work out what we can for max triples for this property
            # AP has no max other than 1 if not repeatable
            if ps["Repeatable"].lower() != "y":
                constr_d["max"] = 1
        # work out value node constraints for this property
        constr_d["valueExpr"] = dict()
        if ps["Type"]:
            constr_d["valueExpr"]["type"] = "NodeConstraint"
            if ps["Type"].lower() == "uri":
                constr_d["valueExpr"]["nodeKind"] = "iri"
            elif ps["Type"].lower() == "literal":
                constr_d["valueExpr"]["nodeKind"] = "literal"
            elif ps["Type"].lower() == "bnode":
                constr_d["valueExpr"]["nodeKind"] = "bnode"
            elif ps["Type"].lower() == "entity":
                constr_d["valueExpr"]["nodeKind"] = "nonliteral"
            else:
                msg = "Warning, found an unexpected constraint type. "
                deets = ps["Type"] + " in statement " + ps["ID"]
                print(msg, deets)
        if ps["Value Space"]:
            # fix me: this is awful.
            value_spaces = ps["Value Space"].split(" ")
            for value_space in value_spaces:
                if value_space[0] == "@":
                    # do something to ref shape
                    key, value = self.process_vs_entity(value_space)
                elif value_space.split(":")[0] in self.namespaces.keys():
                    key, value = self.process_vs_uri(value_space)
                elif value_space.split(":")[0].lower() == "http":
                    key, value = self.process_vs_uri(value_space)
                else:
                    print(value_space, "be not known")
                if key:
                    if type(value) is list:
                        if key in constr_d["valueExpr"]:
                            constr_d["valueExpr"][key].extend(value)
                        else:
                            constr_d["valueExpr"][key] = value
                    else:
                        constr_d["valueExpr"][key] = value
                else:
                    constr_d["valueExpr"] = value
        return constr_d

    def expand_ns(self, uri):
        (ns, name) = uri.split(":")
        if ns in self.namespaces.keys():
            ns_uri = self.namespaces[ns]
            return ns_uri + name
        else:
            return uri

    def process_vs_uri(self, value_space):
        uri = self.expand_ns(value_space)
        if uri.split("#")[0] == "http://www.w3.org/2001/XMLSchema":
            key = "datatype"
            value = uri
        else:
            key = "values"
            value = [uri]
        return key, value

    def process_vs_entity(self, value_space):
        name = value_space[1:]  # drop the '@'
        ns = self.namespaces["shape_ns"]
        uri = ns + ":" + name
        return False, uri

    def dump_j(self):
        print(json.dumps(self.shex_j, indent=4, sort_keys=False))
