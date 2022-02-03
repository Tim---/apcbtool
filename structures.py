#!/usr/bin/env python3

from construct import (
    Int32ul, Int16ul, Int8ul, Bytes, Struct, Rebuild, len_, this, FixedSized,
    GreedyString, Const, OneOf, Terminated, FocusedSeq, GreedyRange, Container,
    ListContainer, PrefixedArray
)

u32 = Int32ul
u16 = Int16ul
u8 = Int8ul


def GreedyRangeTerminated(subcon):
    return FocusedSeq(
        'data',
        'data' / GreedyRange(subcon),
        Terminated,
    )


def PrefixedArrayTerminated(prefix_type, subcon):
    return FocusedSeq(
        'data',
        'data' / PrefixedArray(prefix_type, subcon),
        Terminated,
    )


type_t = Struct(
    'group_id' / u16,
    'type_id' / u16,
    '_size' / Rebuild(u16, len_(this.data) + 0x10),
    'instance' / u16,
    'pad' / Bytes(8),
    'data' / Bytes(this._size - 0x10),
)

types_t = GreedyRangeTerminated(type_t)

group_t = Struct(
    'magic' / FixedSized(4, GreedyString('ascii')),
    'group_id' / u16,
    '_a' / Const(0x10, u16),
    'special' / OneOf(u32, [0x1, 0x01000012]),
    '_size' / Rebuild(u32, len_(this.types) + 0x10),
    'types' / Bytes(this._size - 0x10),
)

groups_t = GreedyRangeTerminated(group_t)

apcb_t = Struct(
    'magic' / Const(b'APCB'),
    'version' / u32,
    '_size' / Rebuild(u32, len_(this.groups) + 0x20),
    'a' / u32,
    'checksum' / u8,
    '_c' / Const(bytes(0xf)),
    'groups' / Bytes(this._size - 0x20),
    Terminated,
)

newtoken_t = Struct(
    'key' / u32,
    'value' / u32
)

newtokens_t = GreedyRangeTerminated(newtoken_t)

# See structure PSCFG_MAXFREQ_ENTRY in Proc/Mem/mp.h
maxfreq_entry_t = Struct(
    'DimmPerCh' / u8,
    Const(0, u8),
    'Dimms' / u16,
    'SR' / u16,
    'DR' / u16,
    'QR' / u16,
    'Speed1_5V' / u16,
    'Speed1_35V' / u16,
    'Speed1_25V' / u16,
)

maxfreq_entries_t = GreedyRangeTerminated(maxfreq_entry_t)

# Related to PSCFG_*_ODTPAT_ENTRY in Proc/Mem/mp.h ?
odtpat_entry_t = Struct(
    'sel' / u32,
    'cs0' / u32,
    'cs1' / u32,
    'cs2' / u32,
    'cs3' / u32,
)

odtpat_entries_t = GreedyRangeTerminated(odtpat_entry_t)

# PSCFG_CADBUS_ENTRY in Proc/Mem/mp.h
cadbus_entry_t = Struct(
    'DimmPerCh' / u32,
    'DDRrate' / u32,
    'VDDIO' / u32,
    'Dimm0' / u32,
    'Dimm1' / u32,
    'GearDownMode' / u16,
    Const(bytes(2)),
    'SlowMode' / u16,
    Const(bytes(2)),
    'AddrCmdCtl' / u32,
    'CkeStrength' / u8,
    'CsOdtStrength' / u8,
    'AddrCmdStrength' / u8,
    'ClkStrength' / u8,
)

cadbus_entries_t = GreedyRangeTerminated(cadbus_entry_t)

# PSCFG_DATABUS_ENTRY in Proc/Mem/mp.h
databus_entry_t = Struct(
    'DimmPerCh' / u32,
    'DDRrate' / u32,
    'VDDIO' / u32,
    'Dimm0' / u32,
    'Dimm1' / u32,
    'RttNom' / u32,
    'RttWr' / u32,
    'RttPark' / u32,
    'DqStrength' / u32,
    'DqsStrength' / u32,
    'OdtStrength' / u32,
    'unknown1' / u32,
    'unknown2' / u32,
)

databus_entries_t = GreedyRangeTerminated(databus_entry_t)


# For each entry
# if value_read & mask == val:
#    return gen
gen_selector_entry_t = Struct(
    'mask' / u8,
    'val' / u8,
    'gen' / u8,
)

# Try to determine the gen using smbus
# A command is sent at the specified address.
# The result is checked against entries
gen_selector_smbus_t = Struct(
    'type' / Const(1, u16),
    Const(bytes(2)),  # On some, it is Bytes(\x00\xff\xff\xff) ?
    'addr' / u16,
    'cmd' / u16,
    'entries' / GreedyRange(gen_selector_entry_t),
)

# Identifies a GPIO
gpio_t = Struct(
    'gpio_num' / u8,
    'mux' / u8,
    'bank' / u8,
)

# Try to determine the gen using GPIOs
# 4 GPIOs are read, and the result stored as a bitmap
# The result is checked against entries
gen_selector_gpio_t = Struct(
    'type' / Const(3, u16),
    'gpios' / gpio_t[4],
    'entries' / GreedyRange(gen_selector_entry_t),
)

# ???
# We add 0x80 to the value, and compare to entries
gen_selector_hardcoded_t = Struct(
    'type' / Const(15, u16),
    'value' / u16,
    'entries' / GreedyRange(gen_selector_entry_t),
)


memg_type34_entry_t = Struct(
    'memclk' / u16,
    'fclk' / u16,
    Const(0xffffffff, u32),
)


memg_type34_entries_t = GreedyRangeTerminated(memg_type34_entry_t)


memg_flags_t = Bytes(0x14)


memg_type30_entry_t = Bytes(540)


memg_type30_entries_t = PrefixedArrayTerminated(u32, memg_type30_entry_t)


memg_type31_entry_t = Bytes(8)


memg_type31_entries_t = GreedyRangeTerminated(memg_type31_entry_t)


def sanitize(obj):
    if isinstance(obj, ListContainer):
        return [
            sanitize(child)
            for child in obj
        ]
    elif isinstance(obj, Container):
        return {
            k: sanitize(v)
            for k, v in obj.items()
            if not k.startswith('_')
        }
    else:
        return obj


debug_port_item_t = Struct(
    'MemOcErrorMask' / u16,
    'PeakMap' / u16,
    'PeakAttr' / u32,
)

debug_port_t = Struct(
    'enabled' / u8,
    'unkown1' / u8,
    'unkown2' / u8,
    'should_read_ack' / u8,
    'rport' / u32,
    'sleep_for_ack' / u32,
    'wport' / u32,
    'unkown3' / u8,
    Const(bytes(3)),
    'write_size' / u32,
    'unkown4' / u32,
    'unkown5' / u32,
    'unkown6' / u32,
    'should_ack_ack' / u8,
    Const(bytes(3)),
    'gpio_pin' / u8,
    'gpio_mux' / u8,
    'gpio_bank_ctl' / u8,
    Const(bytes(1)),
    'items' / debug_port_item_t[8],
    'unkown7' / u8,
    'rest' / Bytes(7),
    Terminated,
)


memg_type53_t = Struct(
    'unknown1' / u8,
    Const(bytes(3)),
    'unknown2' / u32,
    'unknown3' / u32,
    'unknown4' / u32,
    'unknown5' / u32,
    'unknown6' / u32,
    'unknown7' / u32,
    'unknown8' / u8,
    Const(bytes(3)),
)
