from rdflib import Graph
from glob import glob

schema_location = "./schemas/"

def make_base_graph(self):
    """read a load of .ttl RDFS files and merge into a graph"""
    # a more refined version would work out which files are necessary, but thistle do for now
    g = Graph()
    ttl_schema_files = glob(schema_location + "*.ttl")
    for ttl_file in ttl_schema_files:
        try:
            g.parse(location=ttl_file, format="turtle")
        except:
            raise RuntimeError("cannot make graph of " + ttl_file)
    return g
