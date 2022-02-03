#!/usr/bin/env python3

def bin_load_tokens(b):
    assert len(b) % 4 == 0

    # Find split between tokens and data
    for i in range(0, len(b), 4):
        x = int.from_bytes(b[i:i+4], 'little')
        token = x >> 8 & 0x1fff
        if token == 0x1fff:
            break
    else:
        raise Exception('No end of tokens')

    l = [int.from_bytes(b[j:j+4], 'little') for j in range(0, i, 4)]
    payload = b[i+4:]
    cur = 0

    res = []
    for x in l:
        a = (x >> 24 & 0xff)        # 0xff000000
        size = (x >> 21 & 0xf) + 1  # 0x00e00000
        token = x >> 8 & 0x1fff     # 0x001fff00
        b = (x >> 0 & 0xff)         # 0x000000ff

        assert a == 0 and b == 1
        value = int.from_bytes(payload[cur:cur+size], 'little')
        cur += size
        res.append({
            'key': token,
            'value': f'{value:0{size*2}x}',
        })

    # Meh. In some cases we have an extra null byte ?
    lpad, rpad = payload[cur:].split(b'\xff')
    assert not lpad.strip(b'\0')
    assert not rpad.strip(b'\0')
    assert len(rpad) < 4

    return {
        'padding': len(lpad),
        'tokens': res,
    }


def bin_dump_tokens(d):
    part1 = []
    part2 = []

    for token in d['tokens']:
        key = token['key']
        value = int(token['value'], 16)
        size = len(token['value']) // 2

        x = ((size - 1) << 21) | (key << 8) | 1
        part1.append(x.to_bytes(4, 'little'))
        part2.append(value.to_bytes(size, 'little'))

    part1.append((0x1fff << 8).to_bytes(4, 'little'))
    res = b''.join(part1 + part2)
    res += bytes(d['padding']) + b'\xff'
    res += bytes(-len(res) % 4)
    return res
