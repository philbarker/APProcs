from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL
from glob import glob

schema_location = "./schemas/"


def make_base_graph(self):
    """read a load of .ttl RDFS files and mix into a graph"""
    # a more refined version would work out which files are necessary, but thistle do for now
    g = Graph()
    ttl_schema_files = glob(schema_location + "*.ttl")
    for ttl_file in ttl_schema_files:
        try:
            g.parse(location=ttl_file, format="turtle")
        except:
            raise RuntimeError("cannot make graph of " + ttl_file)
    return g


def make_ap_graph(self, base_graph):
    """copy from schema graph those terms that match terms in AP"""
    # a more refined version would have a class of AP Graphs and methods for merging in relevant terms
    namespaces = self["namespaces"]
    entities = self["entities"]
    statements = self["statements"]
    ap_graph = Graph()
    ap_graph = add_ap_namespaces(ap_graph, base_graph, namespaces)
    ap_graph = add_ap_terms(ap_graph, base_graph, entities)
    ap_graph = add_ap_terms(ap_graph, base_graph, statements)
    return ap_graph


def add_ap_namespaces(ap_g, b_g, namespaces):
    # FIXME: put in a check that namespace is in base graph
    # FIXME: put in a check that namespaces copied from base graph are in ap
    for ns in namespaces:
        n = Namespace(ns["Property"])
        p = ns["ID"]
        ap_g.namespace_manager.bind(p, n)
    # functional without this, but aids readability
    ap_g.namespace_manager.bind("owl", OWL, override=False)
    return ap_g


def add_ap_terms(ap_g, b_g, terms):
    # FIXME: not DRY, could generalise from classes & properties to terms
    for term in terms:
        uri = ""
        # separate prefix from name, and match to full namespace URI
        [ns, name] = term["Property"].split(":")
        # FIXME: won't work if no namespace
        for (prefix, ns_uri) in ap_g.namespaces():
            if prefix == ns:
                uri = URIRef(ns_uri + name)
                break
        if "" == uri:
            print("Error did not find namespace %s in base schemas" % ns)
            continue
        else:
            if (uri, None, None) in b_g:
                for (uri, p, o) in b_g.triples((uri, None, None)):
                    ap_g.add((uri, p, o))
                if term["Label"]:
                    ap_g.add((uri, RDFS.label, Literal(term["Label"])))
                if term["Annotation"]:
                    ap_g.add((uri, RDFS.comment, Literal(term["Annotation"])))
            else:
                msg = "Warning did not find term %s:%s in base schemas" % (ns, name)
                print(msg)
                print("Was looking for %s" % uri)

    return ap_g
