# Densha de GO!! Hashiro Yamanote-sen — English Translation Mod

Complete English translation patch for **Densha de GO!! Hashiro Yamanote-sen** (電車でGO！！ はしろう山手線) on Nintendo Switch.

- **Title ID:** `0100BC501355A000`
- **Engine:** Unreal Engine 4 (UE4.25 / Cooked Switch Build)
- **Format:** LayeredFS Mod / Pak Patch (`pakchunk99-Switch.pak` + LocRes)

---

## 🌟 Translation Scope & Coverage

- **100% of In-Game Text:** Over 2,790 strings translated and verified.
- **Accurate Railway Terminology:**
  - Master Controller (マスコン) & Service/Emergency Brake operations.
  - Authentic JR East signaling: Proceed (進行), Caution (注意), Warning (警戒), Stop (停止), Home Signal (場内), Departure Signal (出発), Block Signals (第1～8閉塞).
  - Train dynamics: Acceleration (力行), Coasting (惰行), Constant Speed Zone (定速帯), Stopping Position (停車位置), Point and Call (指差喚呼).
  - Loop directions: Inner Loop (内回り - Counter-clockwise) / Outer Loop (外回り - Clockwise).
- **All Station Names:** Official romanized station names for all 30 Yamanote Line stations, Chuo Line, Sobu Line, and Kansai routes.
- **Complete Menu & UI:** Mode selection, difficulty settings (Beginner, Intermediate, Advanced, Expert), tutorials, mission objectives, driver rankings, evaluations, and dialog popups.

---

## 📦 Installation Instructions

### Option A: Real Hardware (Atmosphere CFW)

1. Connect your Nintendo Switch microSD card to your PC (via USB/FTP/card reader).
2. Copy the `atmosphere` folder from this repository directly to the **root of your microSD card**.
   - Destination path on microSD:
     ```text
     sdmc:/atmosphere/contents/0100BC501355A000/romfs/
     ```
3. If prompted to merge folders or replace files, select **Yes**.
4. Boot into Atmosphere CFW and launch the game. The English text will load automatically!

### Option B: Emulators (Ryujinx / Yuzu / Suyu)

1. Right-click **Densha de GO!! Hashiro Yamanote-sen** in your emulator's game library.
2. Select **Open Mods Directory**.
3. Create a subfolder named `English Translation` (or any name you prefer).
4. Copy the `romfs` folder located inside `atmosphere/contents/0100BC501355A000/` into that folder:
   ```text
   <Mods Directory>/English Translation/romfs/...
   ```
5. Ensure mods are enabled in your emulator settings, and launch the game.

---

## 🛠️ Repository Contents

```text
├── atmosphere/
│   └── contents/
│       └── 0100BC501355A000/
│           └── romfs/
│               └── DgocGame/
│                   └── Content/
│                       ├── Paks/
│                       │   └── pakchunk99-Switch.pak   # Compiled override pak (V8B Zlib)
│                       └── Localization/              # LocRes tables (ja & en cultures)
│                           ├── Game/
│                           └── DgocGame/
├── data/
│   ├── translations_dictionary.json                  # Complete 2,799 bilingual translation mapping
│   └── game_all_texts_en.txt                         # Full translated text dump with UE4 CityHash keys
├── scripts/
│   ├── batch_translate_all.py                        # Neural batch translation script (MarianMT + Glossary)
│   ├── apply_translations_to_locres.py               # Text compiler and string mapper
│   └── create_mod_dist.py                            # LayeredFS mod distributor
└── README.md
```

---

## ⚖️ Disclaimer

This fan translation is not affiliated with, endorsed by, or sponsored by TAITO Corporation, Square Enix, or Nintendo. All trademarks and copyrighted materials belong to their respective owners.
