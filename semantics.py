#!/usr/bin/env python3

import enum


class Version(enum.IntEnum):
    V1 = 0x00200020
    V2 = 0x00300080


class Groups(enum.IntEnum):
    ECB2 = 0x0000
    TOKN = 0x3000
    PSPG = 0x1701
    CCXG = 0x1702
    DFG  = 0x1703
    MEMG = 0x1704
    GNBG = 0x1705
    FCHG = 0x1706
    CBSG = 0x1707


known_types = {
    Version.V1: {
        Groups.PSPG: {
            0x01: 'tokens',
            0x02: 'tokens',
            # TODO: PSPG 0x60 should use the gen_selector_*_t structures
            0x60: 'raw',
        },
        Groups.CCXG: {
            0x03: 'tokens',
            0x04: 'tokens',
        },
        Groups.DFG: {
            0x05: 'tokens',
            0x06: 'tokens',
        },
        Groups.MEMG: {
            0x07: 'tokens',
            0x08: 'tokens',
        },
        Groups.GNBG: {
            0x09: 'tokens',
            0x0a: 'tokens',
        },
        Groups.FCHG: {
            0x0b: 'tokens',
            0x0c: 'tokens',
        },
        Groups.CBSG: {
            0x0d: 'tokens',
            0x0f: 'tokens',
        },
    },
    Version.V2: {
        Groups.PSPG: {
            # TODO: PSPG 0x60 should use the gen_selector_*_t structures
            0x60: 'raw',
        },
        Groups.TOKN: {
            0x00: 'newtokens',
            0x01: 'newtokens',
            0x02: 'newtokens',
            0x04: 'newtokens',
        },
        Groups.MEMG: {
            # Mostly TODO
            0x30: 'memg_type30',
            0x31: 'memg_type31',
            0x34: 'memg_type34',
            0x50: 'memg_flags',
            0x52: 'debugport',
            0x53: 'memg_type53',

            # # Maxfreq
            # UDIMM
            0x44: 'maxfreq',
            0x45: 'maxfreq',
            # LRDIMM
            0x49: 'maxfreq',
            0x4a: 'maxfreq',
            # SO DIMM
            0x4b: 'maxfreq',
            0x4c: 'maxfreq',
            # RDIMM
            0x57: 'maxfreq',
            0x58: 'maxfreq',
            # 3DS DIMM
            0x5c: 'maxfreq',
            0x5d: 'maxfreq',

            # # ODT Pattern
            # UDIMM
            0x41: 'odtpat',
            # RDIMM
            0x46: 'odtpat',
            # LRDimm
            0x54: 'odtpat',
            # SO DIMM
            0x59: 'odtpat',

            # # CAD BUS
            # UDIMM
            0x42: 'cadbus',
            # RDIMM
            0x47: 'cadbus',
            # LRDimm
            0x55: 'cadbus',
            # SO DIMM
            0x5a: 'cadbus',

            # TODO: only works for V2 ?
            # # Data bus config
            # UDIMM
            0x43: 'databus',
            # LRDIMM
            0x56: 'databus',
            # SO DIMM
            0x5b: 'databus',
            # RDIMM
            0x48: 'databus',
            # 3DS DIMM
            0x4d: 'databus',
        },
    },
}
