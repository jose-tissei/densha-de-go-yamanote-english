import os
import shutil

staging_dir = r"C:\git\densha-ts\work\staging\DgocGame\Content\Localization"
os.makedirs(os.path.join(staging_dir, "Game", "ja"), exist_ok=True)
os.makedirs(os.path.join(staging_dir, "Game", "en"), exist_ok=True)
os.makedirs(os.path.join(staging_dir, "DgocGame", "ja"), exist_ok=True)
os.makedirs(os.path.join(staging_dir, "DgocGame", "en"), exist_ok=True)

locres_src = r"C:\git\densha-ts\work\Game.locres"

# Copy Game.locres to all relevant culture and project paths
shutil.copy(locres_src, os.path.join(staging_dir, "Game", "ja", "Game.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "Game", "en", "Game.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "Game", "ja", "DgocGame.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "Game", "en", "DgocGame.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "DgocGame", "ja", "Game.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "DgocGame", "en", "Game.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "DgocGame", "ja", "DgocGame.locres"))
shutil.copy(locres_src, os.path.join(staging_dir, "DgocGame", "en", "DgocGame.locres"))

print("Staged all localization files successfully!")
