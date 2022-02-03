#!/usr/bin/env python3

import argparse
from bin_serializer import bin_load, bin_dump
from yaml_serializer import yaml_load, yaml_dump


def check_sanity(raw):
    apcb = bin_load(raw)
    y = yaml_dump(apcb)
    apcb2 = yaml_load(y)
    raw2 = bin_dump(apcb2)
    assert raw == raw2


def dump(raw):
    apcb = bin_load(raw)
    y = yaml_dump(apcb)
    print(y)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('rb'))
    parser.add_argument('--check-sanity', action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    raw = args.file.read()
    if args.check_sanity:
        check_sanity(raw)
    dump(raw)


if __name__ == "__main__":
    main()
