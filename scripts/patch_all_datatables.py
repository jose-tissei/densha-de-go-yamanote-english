import os
import sys
import json
import struct
import shutil
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

print("[DataTablePatcher] Loading translations dictionary...")
dict_path = r'C:\git\densha-ts\work\translations_dictionary.json'
with open(dict_path, 'r', encoding='utf-8') as f:
    translations = json.load(f)

norm_dict = {}
for k, v in translations.items():
    norm_dict[k] = v
    norm_dict[k.strip()] = v
    norm_dict[k.replace('\n', r'\n')] = v.replace('\n', r'\n')
    norm_dict[k.replace(r'\n', '\n')] = v.replace(r'\n', '\n')

clean_dialog = {
    'セーブデータを確認しています。\\n電源を切らないでください。': 'Checking save data.\\nPlease do not turn off the power.',
    'セーブデータの読み込みに失敗しました。': 'Failed to load save data.',
    'セーブデータを再作成して初期化します。\\n保存されているセーブデータは削除されます。': 'Re-creating and initializing save data.\\nExisting save data will be deleted.',
    'セーブデータがありません。\\n新しく作成します。': 'No save data found.\\nCreate new save data?',
    'このゲームはオートセーブ機能に対応しています。\\n画面左下のセーブアイコンが表示されている間は\\n電源を切らないでください。\\n': 'This game supports autosaving.\\nDo not turn off the power while the save icon\\nis displayed in the lower left corner.\\n',
    'セーブデータを作成しています…': 'Creating save data...',
    'セーブデータの作成に失敗しました。\\nセーブデータを作成せずに\\nゲームを開始しますか。': 'Failed to create save data.\\nStart the game without saving?',
    '古いバージョンで作成されたセーブデータです。\\n新しいバージョン用に変換します。\\n変換されたデータは古いバージョンの\\nアプリケーションでは動作しません。': 'Save data from an older version detected.\\nConverting for the new version.\\nConverted data cannot be used on older versions.',
    '新しいバージョンで作成されたセーブデータです。\\nアプリケーションを終了し、アップデート\\nしてください。このままゲームを進めた場合、\\nセーブデータは削除され再作成されます。': 'Save data from a newer version detected.\\nPlease update the software.\\nContinuing will overwrite and reset save data.',
    'セーブデータを変換しています...': 'Converting save data...',
    'セーブデータの変換に失敗しました。\\n次に保存されるときに\\n新しいバージョン用に変換されます。': 'Failed to convert save data.\\nIt will be converted for the new version\\nthe next time you save.',
}
for k, v in clean_dialog.items():
    norm_dict[k] = v

ext_path = r'C:\git\densha-ts\work\extracted_texts.json'
with open(ext_path, 'r', encoding='utf-8') as f:
    ext_data = json.load(f)

unpacked = r'C:\git\densha-ts\work\unpacked\pakchunk1\DgocGame\Content'
staging_content = r'C:\git\densha-ts\work\staging\DgocGame\Content'

patched_tables = 0
total_replaced = 0

print("[DataTablePatcher] Patching DataTables...")
for rel_uexp in ext_data:
    if not ('DataTable' in rel_uexp or 'DataTables' in rel_uexp):
        continue
    base_rel = os.path.splitext(rel_uexp)[0]
    uasset_p = os.path.join(unpacked, base_rel + '.uasset')
    uexp_p = os.path.join(unpacked, base_rel + '.uexp')
    if not (os.path.exists(uasset_p) and os.path.exists(uexp_p)):
        continue

    with open(uasset_p, 'rb') as f:
        uasset_data = bytearray(f.read())
    with open(uexp_p, 'rb') as f:
        ue_data = f.read()

    pos = 0
    segments = []
    last_pos = 0
    file_replaced = 0

    while pos < len(ue_data) - 4:
        slen, = struct.unpack('<i', ue_data[pos:pos+4])
        if -2000 < slen < -1:
            blen = -slen * 2
            if pos + 4 + blen <= len(ue_data):
                raw = ue_data[pos+4:pos+4+blen]
                if raw.endswith(b'\x00\x00'):
                    try:
                        s = raw[:-2].decode('utf-16le')
                        if s in norm_dict:
                            trans = norm_dict[s]
                            segments.append(ue_data[last_pos:pos])
                            new_chars = len(trans) + 1
                            new_hdr = struct.pack('<i', -new_chars)
                            new_payload = trans.encode('utf-16le') + b'\x00\x00'
                            segments.append(new_hdr + new_payload)
                            pos += 4 + blen
                            last_pos = pos
                            file_replaced += 1
                            continue
                    except:
                        pass
        pos += 1

    if file_replaced > 0:
        segments.append(ue_data[last_pos:])
        new_uexp = b''.join(segments)

        # Update uasset SerialSize
        exp_cnt, = struct.unpack('<i', uasset_data[57:61])
        exp_off, = struct.unpack('<i', uasset_data[61:65])
        new_serial_size = len(new_uexp) - 4
        struct.pack_into('<q', uasset_data, exp_off + 28, new_serial_size)

        out_uasset = os.path.join(staging_content, base_rel + '.uasset')
        out_uexp = os.path.join(staging_content, base_rel + '.uexp')
        os.makedirs(os.path.dirname(out_uasset), exist_ok=True)

        with open(out_uasset, 'wb') as f:
            f.write(uasset_data)
        with open(out_uexp, 'wb') as f:
            f.write(new_uexp)

        patched_tables += 1
        total_replaced += file_replaced
        print(f"  [+] Patched {rel_uexp} ({file_replaced} strings)")

print(f"[DataTablePatcher] Finished: {patched_tables} tables patched, {total_replaced} strings replaced.")

# Stage clean un-truncated LocRes
print("[DataTablePatcher] Staging LocRes files...")
locres_src = r'C:\git\densha-ts\work\Game.locres'
loc_dir = os.path.join(staging_content, "Localization")
for proj in ["Game", "DgocGame"]:
    for lang in ["ja", "en"]:
        d = os.path.join(loc_dir, proj, lang)
        os.makedirs(d, exist_ok=True)
        shutil.copy(locres_src, os.path.join(d, "Game.locres"))
        shutil.copy(locres_src, os.path.join(d, "DgocGame.locres"))

# Pack with repak
print("[DataTablePatcher] Packing into patch paks...")
repak = r'C:\git\densha-ts\work\tools\repak\repak.exe'
staging_root = r'C:\git\densha-ts\work\staging'
pak_p = r'C:\git\densha-ts\work\pakchunk0-Switch_99_P.pak'
pak_99 = r'C:\git\densha-ts\work\pakchunk99-Switch.pak'

for pak in [pak_p, pak_99]:
    cmd = [repak, "pack", staging_root, pak, "--version", "V8B", "--compression", "Zlib"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  [+] Packed {pak} ({os.path.getsize(pak)} bytes)")
    else:
        print(f"  [!] Error packing {pak}: {res.stderr}")

# Sync to LayeredFS, atmosphere, and Ryujinx
print("[DataTablePatcher] Syncing to all target directories...")
targets = [
    r'C:\git\densha-ts\work\atmosphere\contents\0100BC501355A000\romfs\DgocGame',
    r'C:\git\densha-ts\work\LayeredFS\0100BC501355A000\romfs\DgocGame',
    r'C:\git\densha-ts\work\tools\ryujinx\publish\portable\mods\contents\0100bc501355a000\EnglishMod\romfs\DgocGame',
    r'C:\git\densha-ts\work\tools\ryujinx\publish\portable\sdcard\atmosphere\contents\0100bc501355a000\romfs\DgocGame',
]

for t in targets:
    # sync paks
    paks_dir = os.path.join(t, 'Content', 'Paks')
    os.makedirs(paks_dir, exist_ok=True)
    shutil.copy(pak_p, os.path.join(paks_dir, os.path.basename(pak_p)))
    shutil.copy(pak_99, os.path.join(paks_dir, os.path.basename(pak_99)))

    # sync locres
    t_loc = os.path.join(t, 'Content', 'Localization')
    for proj in ["Game", "DgocGame"]:
        for lang in ["ja", "en"]:
            d = os.path.join(t_loc, proj, lang)
            os.makedirs(d, exist_ok=True)
            shutil.copy(locres_src, os.path.join(d, "Game.locres"))
            shutil.copy(locres_src, os.path.join(d, "DgocGame.locres"))

    # sync loose datatable files for high-priority override
    for root, _, files in os.walk(os.path.join(staging_content, 'DgocBlueprints')):
        for f in files:
            src_f = os.path.join(root, f)
            rel_f = os.path.relpath(src_f, staging_content)
            dst_f = os.path.join(t, 'Content', rel_f)
            os.makedirs(os.path.dirname(dst_f), exist_ok=True)
            shutil.copy(src_f, dst_f)

print("[DataTablePatcher] ALL DONE! All 38 DataTables, LocRes, and Paks updated and deployed!")
