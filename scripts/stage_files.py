import os
import shutil
import subprocess

staging_root = r"C:\git\densha-ts\work\staging"
# Recreate clean staging directory
if os.path.exists(staging_root):
    shutil.rmtree(staging_root)

staging_dir = os.path.join(staging_root, "DgocGame", "Content", "Localization")
os.makedirs(os.path.join(staging_dir, "Game", "ja"), exist_ok=True)
os.makedirs(os.path.join(staging_dir, "Game", "en"), exist_ok=True)
os.makedirs(os.path.join(staging_dir, "DgocGame", "ja"), exist_ok=True)
os.makedirs(os.path.join(staging_dir, "DgocGame", "en"), exist_ok=True)

locres_src = r"C:\git\densha-ts\work\Game.locres"

# Copy Game.locres to all relevant culture and project paths
for proj in ["Game", "DgocGame"]:
    for lang in ["ja", "en"]:
        target_dir = os.path.join(staging_dir, proj, lang)
        shutil.copy(locres_src, os.path.join(target_dir, "Game.locres"))
        shutil.copy(locres_src, os.path.join(target_dir, "DgocGame.locres"))

print(f"Staged all localization files successfully (locres size: {os.path.getsize(locres_src)} bytes)!")

# Pack using repak into both pakchunk0-Switch_99_P.pak and pakchunk99-Switch.pak
repak_exe = r"C:\git\densha-ts\work\tools\repak\repak.exe"

pak_p = r"C:\git\densha-ts\work\pakchunk0-Switch_99_P.pak"
pak_99 = r"C:\git\densha-ts\work\pakchunk99-Switch.pak"

for out_pak in [pak_p, pak_99]:
    cmd = [repak_exe, "pack", staging_root, out_pak, "--version", "V8B", "--compression", "Zlib"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Created pak: {out_pak}, Size: {os.path.getsize(out_pak)} bytes")
    else:
        print(f"Error creating {out_pak}: {res.stderr}")
