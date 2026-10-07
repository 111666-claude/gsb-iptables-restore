"""命令行入口。"""

import argparse

from . import samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="iptables")
    ap.add_argument("--sample", choices=["table", "policy", "dup", "counter", "work"])
    args = ap.parse_args(argv)
    if args.sample:
        return samples.run(args.sample)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
