# Troubleshooting Guide: LayeredFS & Mod Loading

This guide provides step-by-step diagnostics to verify that your Nintendo Switch is correctly running Atmosphère CFW, that LayeredFS is active, and that the English Translation Mod files are properly recognized.

---

## 1. How LayeredFS Works on Nintendo Switch

**LayeredFS (`fs.mitm`) is built directly into Atmosphère and is ENABLED BY DEFAULT.**
- You do **not** need to edit `override_config.ini`, `system_settings.ini`, or any other config file to turn it on.
- Modifying these config files without need can inadvertently disable mod loading or break the Homebrew Menu loader.

---

## 2. Step-by-Step Diagnostic Checklist

### Step A: Verify Atmosphère CFW is Actually Running
If your console boots into Stock OFW (Official Firmware) instead of CFW, LayeredFS will not function.
1. Power on your Switch and open **System Settings** (gear icon on the home screen).
2. Scroll to the bottom and select **System**.
3. Check the text beneath **System Update**:
   - ✅ **CFW Active:** It will display `Current version: XX.X.X|AMS X.X.X|S` (or `|E` for emuMMC).
   - ❌ **Stock OFW:** It will only display `Current version: XX.X.X` without `|AMS`. If you see this, reboot your console into RCM and inject the Hekate / Fusee payload to boot into Atmosphère.

---

### Step B: Do Not Hold the `L` Button When Launching
In standard Atmosphère configurations:
- Holding the **`L`** button while launching a game triggers the bypass override.
- This **disables LayeredFS** for that game launch, running the completely unmodded base game.
- Always tap the game icon normally without holding any shoulder buttons.

---

### Step C: Verify the MicroSD Folder Structure
Atmosphère requires an exact path structure based on the game's Title ID:
- **Title ID:** `0100BC501355A000` (Densha de GO!! Hashiro Yamanote-sen)

Ensure your microSD card matches this exact hierarchy:
```text
sdmc:/
└── atmosphere/
    └── contents/
        └── 0100BC501355A000/
            └── romfs/
                └── DgocGame/
                    ├── Config/
                    │   └── Switch/
                    │       └── SwitchEngine.ini
                    └── Content/
                        ├── Localization/
                        │   ├── Game/
                        │   │   ├── ja/
                        │   │   │   ├── Game.locres
                        │   │   │   └── DgocGame.locres
                        │   │   └── en/
                        │   │       ├── Game.locres
                        │   │       └── DgocGame.locres
                        │   └── DgocGame/
                        │       ├── ja/
                        │       └── en/
                        └── Paks/
                            ├── pakchunk0-Switch_99_P.pak
                            └── pakchunk99-Switch.pak
```

#### Common Path Pitfalls:
- **`titles` vs `contents`:** Do not use `atmosphere/titles/`. That directory was deprecated in Atmosphère 0.10.0 (2019). Modern versions strictly use `atmosphere/contents/`.
- **Nested Folder Duplication:** Check that extracting the mod didn't create duplicate folders, such as `atmosphere/atmosphere/...` or `contents/0100BC501355A000/0100BC501355A000/...`.
- **Disable Flag:** Check if `atmosphere/contents/0100BC501355A000/flags/disable_mitm` exists. If this file is present, Atmosphère disables LayeredFS for this title. Delete the `flags` folder if present.

---

### Step D: Fix the Archive Bit (Crucial on Windows & macOS)
When copying files to a FAT32 or exFAT microSD card from a PC or Mac, the filesystem's **archive bit** flag frequently gets set on folders. 

Nintendo's Horizon OS cannot read folders with the archive bit set, causing Atmosphère to silently ignore the mod directory.

#### How to fix:
1. Turn off your Switch and boot into **Hekate**.
2. Tap **Tools** at the top.
3. Tap **Arch bit • RCM • Touch** in the bottom right corner.
4. Tap **Fix Archive Bit**.
5. Wait for the process to complete (it scans all files and folders on your SD card).
6. Reboot back into Atmosphère CFW.

---

### Step E: 60-Second Sanity Test for LayeredFS
If you want to verify 100% whether LayeredFS is redirecting files for this game:
1. Connect your microSD to your computer (or via FTP / DBI / Hekate USB).
2. Navigate to:
   ```text
   sdmc:/atmosphere/contents/0100BC501355A000/romfs/DgocGame/Content/Movies/
   ```
3. Create a new, empty (0-byte) text file and name it `OpeningMovie.usm`.
4. Launch the game on your Switch:
   - **If LayeredFS works:** The opening cinematic will immediately be skipped or display a black screen.
   - **If LayeredFS is not working:** The standard intro movie will play normally.
5. After testing, delete `OpeningMovie.usm` to restore the movie.

---

## 3. Unreal Engine 4 Specific Notes

### Japanese Culture Fallback
*Densha de GO!!* was developed as a Japan-only release. In the game's internal `SwitchEngine.ini`, English was explicitly excluded:
```ini
-SupportedLanguages=AmericanEnglish
+SupportedLanguages=Japanese
```
Because of this:
- The game will default to the `ja` (Japanese) culture even when your Nintendo Switch system language is set to English.
- The mod handles this by supplying the translated `Game.locres` in **both `ja` and `en`** localization folders, as well as providing an updated `SwitchEngine.ini` override.

### Patch Pak Naming (`_P.pak`)
Unreal Engine 4 mounts `.pak` files in alphanumeric order, but gives absolute priority to packages containing the `_P` (Patch) suffix.
- This release packages the translation as `pakchunk0-Switch_99_P.pak` to ensure the engine mounts the translated assets with top priority over the base game chunks (`pakchunk0` through `pakchunk16`).
- A backup `pakchunk99-Switch.pak` and loose `.locres` files are also included for complete fallback coverage.
