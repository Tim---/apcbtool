#!/usr/bin/env python3

from structures import groups_t
from type_serdes import bin_load_types, bin_dump_types
from semantics import Groups


def bin_load_group(version, o):
    # There is a 1 to 1 mapping between group_id and magic
    magic = o.magic.rstrip(' ')
    group_type = Groups[magic]
    assert group_type.value == o.group_id

    if group_type == Groups.ECB2:
        # Special case: raw data
        assert o.special == 0x01000012
        res = o.types.hex()
    else:
        # Normal case: types
        assert o.special == 1
        res = bin_load_types(version, group_type, o.types)

    return group_type.name, res


def bin_dump_group(version, group_name, group):
    group_type = Groups[group_name]

    if group_type == Groups.ECB2:
        # Special case: raw data
        special = 0x01000012
        types = bytes.fromhex(group)
    else:
        # Normal case: types
        special = 1
        types = bin_dump_types(version, group_type, group)

    return {
        'magic': group_type.name.ljust(4),
        'group_id': group_type.value,
        'special': special,
        'types': types,
    }


def bin_load_groups(version, b):
    return dict(bin_load_group(version, o) for o in groups_t.parse(b))


def bin_dump_groups(version, groups):
    return groups_t.build(
        bin_dump_group(version, group_name, g)
        for group_name, g in groups.items()
    )
