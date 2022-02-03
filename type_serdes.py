#!/usr/bin/env python3

from structures import (
    types_t, maxfreq_entries_t, sanitize, newtokens_t, odtpat_entries_t,
    cadbus_entries_t, databus_entries_t, memg_type34_entries_t, memg_flags_t,
    memg_type30_entries_t, memg_type31_entries_t, debug_port_t, memg_type53_t,
)
from token_serdes import bin_load_tokens, bin_dump_tokens
from semantics import Version, known_types


def get_parser(version, group_type, type_id):
    types = known_types[version]
    if group_type not in types:
        return 'raw'
    if type_id not in types[group_type]:
        return 'raw'
    return types[group_type][type_id]


def struct_parser(s):
    return {
        'load': lambda data: sanitize(s.parse(data)),
        'dump': lambda data: s.build(data),
    }


type_parsers = {
    'newtokens':    struct_parser(newtokens_t),
    'maxfreq':      struct_parser(maxfreq_entries_t),
    'odtpat':       struct_parser(odtpat_entries_t),
    'cadbus':       struct_parser(cadbus_entries_t),
    'databus':      struct_parser(databus_entries_t),
    'memg_type30':  struct_parser(memg_type30_entries_t),
    'memg_type31':  struct_parser(memg_type31_entries_t),
    'memg_type34':  struct_parser(memg_type34_entries_t),
    'memg_type53':  struct_parser(memg_type53_t),
    'memg_flags':   struct_parser(memg_flags_t),
    'debugport':    struct_parser(debug_port_t),
    'tokens': {
        'load': bin_load_tokens,
        'dump': bin_dump_tokens
    },
    'raw': {
        'load': lambda data: data.hex(),
        'dump': lambda data: bytes.fromhex(data)
    },
}


def bin_load_type(version, group_type, o):
    assert o.group_id == group_type.value

    parser = get_parser(version, group_type, o.type_id)
    data = type_parsers[parser]['load'](o.data)

    res = {
        'type_id': o.type_id,
        'instance': o.instance,
        'data': data,
    }

    if version != Version.V1:
        res['pad'] = o.pad.hex()

    return res


def bin_dump_type(version, group_type, type_):
    parser = get_parser(version, group_type, type_['type_id'])
    data = type_parsers[parser]['dump'](type_['data'])

    pad = bytes(8) if version == Version.V1 else bytes.fromhex(type_['pad'])

    res = {
        'group_id': group_type.value,
        'type_id': type_['type_id'],
        'instance': type_['instance'],
        'pad': pad,
        'data': data,
    }
    return res


def bin_load_types(version, group_type, b):
    return [bin_load_type(version, group_type, o) for o in types_t.parse(b)]


def bin_dump_types(version, group_type, types):
    return types_t.build(bin_dump_type(version, group_type, t) for t in types)
