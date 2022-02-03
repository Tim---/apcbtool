#!/usr/bin/env python3

from structures import apcb_t
from group_serdes import bin_load_groups, bin_dump_groups
from semantics import Version


def bin_load_apcb(b):
    o = apcb_t.parse(b)
    version = Version(o.version)

    valid_checksum = sum(b) % 256 == 0
    if not valid_checksum:
        assert o.checksum == 0

    return {
        'version': version.name,
        'a': o.a,
        'valid_checksum': valid_checksum,
        'groups': bin_load_groups(version, o.groups)
    }


def bin_dump_apcb(apcb):
    version = Version[apcb['version']]

    d = {
        'version': version.value,
        'a': apcb['a'],
        'checksum': 0,
        'groups': bin_dump_groups(version, apcb['groups']),
    }

    raw = apcb_t.build(d)
    if not apcb['valid_checksum']:
        return raw

    d['checksum'] = (-sum(raw)) % 256
    raw = apcb_t.build(d)

    return raw
