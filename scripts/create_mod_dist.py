import os
import shutil

base_romfs = r"C:\git\densha-ts\work\LayeredFS\0100BC501355A000\romfs\DgocGame"
content_dir = os.path.join(base_romfs, "Content")
paks_out = os.path.join(content_dir, "Paks")
loc_out = os.path.join(content_dir, "Localization")

# Clean and recreate LayeredFS directory
if os.path.exists(r"C:\git\densha-ts\work\LayeredFS"):
    shutil.rmtree(r"C:\git\densha-ts\work\LayeredFS")

os.makedirs(paks_out, exist_ok=True)

# Copy both patch pak and fallback pak
for pak_name in ["pakchunk0-Switch_99_P.pak", "pakchunk99-Switch.pak"]:
    pak_src = os.path.join(r"C:\git\densha-ts\work", pak_name)
    if os.path.exists(pak_src):
        shutil.copy(pak_src, os.path.join(paks_out, pak_name))

# Copy loose locres files
locres_src = r"C:\git\densha-ts\work\Game.locres"
for proj in ["Game", "DgocGame"]:
    for lang in ["ja", "en"]:
        d = os.path.join(loc_out, proj, lang)
        os.makedirs(d, exist_ok=True)
        shutil.copy(locres_src, os.path.join(d, "Game.locres"))
        shutil.copy(locres_src, os.path.join(d, "DgocGame.locres"))

# Recreate atmosphere directory structure
if os.path.exists(r"C:\git\densha-ts\work\atmosphere"):
    shutil.rmtree(r"C:\git\densha-ts\work\atmosphere")
shutil.copytree(r"C:\git\densha-ts\work\LayeredFS\0100BC501355A000", r"C:\git\densha-ts\work\atmosphere\contents\0100BC501355A000")

print("Created clean LayeredFS and atmosphere structures successfully without modifying Config/SwitchEngine.ini!")
