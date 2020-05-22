from approcs import APProcs
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Read an application profile from simple csv file and output some RDFS for the profile.",
    )
    parser.add_argument(
        "-if",
        "--infile",
        type=str,
        default="input/ap_bookclub.csv",
        help="input file name of Application Profile csv",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    ap = APProcs(args.infile)
    ap.dump()
#    yama = ap.build_yama()
    #    print(ap.yaml.dump(yama, default_flow_style=False))
#    base = ap.make_base_graph()
#    ap_graph = ap.make_ap_graph(base)
#    print(ap_graph.serialize(format="turtle").decode("utf-8"))
