from approcs import AP
import argparse
from approcs.yama_utils import build_yama, dump_yama
from approcs.shex_utils import ShexAP

# from approcs.rdfs_utils import make_base_graph, make_ap_graph


def get_args():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Read an application profile from simple csv file and output some RDFS for the profile.",
        epilog="Please note, this is unfinished and buggy.",
    )
    parser.add_argument(
        "infile",
        type=str,
        default="input/ap_bookclub.csv",
        help="input file name of Application Profile csv",
    )
    parser.add_argument(
        "-d", "--dump", action="store_true", help="Dump (print) the AP once loaded"
    )
    parser.add_argument(
        "-y",
        "--yama",
        action="store_true",
        help="Convert and dump (print) the AP as YAMA",
    )
    parser.add_argument(
        "-s",
        "--shex",
        action="store_true",
        help="Convert and dump (print) the AP as shexj",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    ap = AP(args.infile)
    if args.dump:
        ap.dump()
    if args.yama:
        yama = build_yama(ap)
        dump_yama(yama)
    if args.shex:
        shex = ShexAP(ap)
        shex.dump_j()
#    base = ap.make_base_graph()
#    ap_graph = ap.make_ap_graph(base)
#    print(ap_graph.serialize(format="turtle").decode("utf-8"))
