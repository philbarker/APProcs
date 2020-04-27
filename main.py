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
        default="input/nishad.csv",
        help="input file name of Application Profile csv",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    ap = APProcs(args.infile)
    ap.dump(["entities", "statements"])
    yama = APProcs.build_yama(ap)
    print(APProcs.yaml.dump(yama, default_flow_style=False))
    base = APProcs.make_base_graph()
