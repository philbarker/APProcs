from approcs import APProcs
import argparse
from approcs.yama_utils import build_yama, dump_yama
from approcs.rdfs_utils import make_base_graph, make_ap_graph


def get_args():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Read an application profile from simple csv file and output some RDFS for the profile.",
    )
    parser.add_argument(
        "infile",
        type=str,
        default="input/ap_bookclub.csv",
        help="input file name of Application Profile csv",
    )
    parser.add_argument(
        "-d",
        "--dump",
        type=str,
        default="False",
        help="Dump (print) the AP once loaded",
    )
    parser.add_argument(
        "-y",
        "--yama",
        type=str,
        default="False",
        help="Convert and dump (print) the AP as YAMA",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    ap = APProcs(args.infile)
    if args.dump.lower() in ["true", "t", "1", "y", "yes"]:
        ap.dump()
    if args.yama.lower() in ["true", "t", "1", "y", "yes"]:
        yama = build_yama(ap)
        dump_yama(yama)
#    base = ap.make_base_graph()
#    ap_graph = ap.make_ap_graph(base)
#    print(ap_graph.serialize(format="turtle").decode("utf-8"))
