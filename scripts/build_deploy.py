import os, shutil, subprocess, sys
W = r'C:\git\densha-ts\work'
repak = f'{W}/tools/repak/repak.exe'
staging = f'{W}/staging'
paks = [f'{W}/pakchunk0-Switch_99_P.pak', f'{W}/pakchunk99-Switch.pak']
for p in paks:
    r = subprocess.run([repak, 'pack', staging, p, '--version', 'V8B', '--compression', 'Zlib'], capture_output=True, text=True)
    print('pack', os.path.basename(p), r.returncode, os.path.getsize(p) if os.path.exists(p) else None, r.stderr[-200:])
    if r.returncode: sys.exit(1)
targets = [
    f'{W}/atmosphere/contents/0100BC501355A000/romfs/DgocGame',
    f'{W}/LayeredFS/0100BC501355A000/romfs/DgocGame',
    f'{W}/tools/ryujinx/publish/portable/mods/contents/0100bc501355a000/EnglishMod/romfs/DgocGame',
    f'{W}/tools/ryujinx/publish/portable/sdcard/atmosphere/contents/0100bc501355a000/romfs/DgocGame',
]
for t in targets:
    d = f'{t}/Content/Paks'; os.makedirs(d, exist_ok=True)
    for p in paks: shutil.copy(p, f'{d}/{os.path.basename(p)}')
print('deployed to', len(targets), 'targets')
