import os
import shutil

base_out = r"C:\git\densha-ts\work\LayeredFS\0100BC501355A000\romfs\DgocGame\Content"
paks_out = os.path.join(base_out, "Paks")
loc_out = os.path.join(base_out, "Localization")

os.makedirs(paks_out, exist_ok=True)
os.makedirs(os.path.join(loc_out, "Game", "ja"), exist_ok=True)
os.makedirs(os.path.join(loc_out, "Game", "en"), exist_ok=True)
os.makedirs(os.path.join(loc_out, "DgocGame", "ja"), exist_ok=True)
os.makedirs(os.path.join(loc_out, "DgocGame", "en"), exist_ok=True)

# Copy pak
pak_src = r"C:\git\densha-ts\work\pakchunk99-Switch.pak"
shutil.copy(pak_src, os.path.join(paks_out, "pakchunk99-Switch.pak"))

# Copy loose locres
locres_src = r"C:\git\densha-ts\work\Game.locres"
shutil.copy(locres_src, os.path.join(loc_out, "Game", "ja", "Game.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "Game", "en", "Game.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "Game", "ja", "DgocGame.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "Game", "en", "DgocGame.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "DgocGame", "ja", "Game.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "DgocGame", "en", "Game.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "DgocGame", "ja", "DgocGame.locres"))
shutil.copy(locres_src, os.path.join(loc_out, "DgocGame", "en", "DgocGame.locres"))

# Also create atmosphere directory structure
atmo_dir = r"C:\git\densha-ts\work\atmosphere\contents\0100BC501355A000\romfs\DgocGame\Content"
if os.path.exists(r"C:\git\densha-ts\work\atmosphere"):
    shutil.rmtree(r"C:\git\densha-ts\work\atmosphere")
shutil.copytree(r"C:\git\densha-ts\work\LayeredFS\0100BC501355A000", r"C:\git\densha-ts\work\atmosphere\contents\0100BC501355A000")

print("Created LayeredFS and atmosphere structures successfully!")
