import os, sys, json, struct
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:\git\densha-ts\work'
UNP = f'{W}/unpacked/pakchunk1/DgocGame/Content'
STG = f'{W}/staging/DgocGame/Content'
FILES = sys.argv[1:] or ['DgocGameData/SupportInfo/DgocSupportInfo']

tr = json.load(open(f'{W}/translations_dictionary.json', encoding='utf-8'))
norm = {}
for k, v in tr.items():
    norm[k] = v; norm[k.strip()] = v
    norm[k.replace('\n', '\\n')] = v.replace('\n', '\\n')

for rel in FILES:
    ua = bytearray(open(f'{UNP}/{rel}.uasset', 'rb').read())
    ue = open(f'{UNP}/{rel}.uexp', 'rb').read()
    pos = last = 0; seg = []; n = 0; miss = []
    while pos < len(ue) - 4:
        sl = struct.unpack_from('<i', ue, pos)[0]
        if -3000 < sl < -1:
            e = pos + 4 + (-sl) * 2
            if e <= len(ue) and ue[e - 2:e] == b'\0\0':
                try:
                    s = ue[pos + 4:e - 2].decode('utf-16le')
                    if s in norm:
                        t = norm[s]
                        seg.append(ue[last:pos]); seg.append(struct.pack('<i', -(len(t) + 1)) + t.encode('utf-16le') + b'\0\0')
                        pos = last = e; n += 1; continue
                except Exception:
                    pass
        pos += 1
    seg.append(ue[last:])
    new = b''.join(seg)
    exp_off, = struct.unpack_from('<i', ua, 61)
    struct.pack_into('<q', ua, exp_off + 28, len(new) - 4)
    out = f'{STG}/{rel}'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out + '.uasset', 'wb').write(ua); open(out + '.uexp', 'wb').write(new)
    print('patched', rel, n, 'strings')
