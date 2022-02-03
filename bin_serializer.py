#!/usr/bin/env python3

from apcb_serdes import bin_load_apcb, bin_dump_apcb


def bin_load(b):
    return bin_load_apcb(b)


def bin_dump(o):
    return bin_dump_apcb(o)
