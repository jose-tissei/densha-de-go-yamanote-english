import json
import re
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

dict_path = r"C:\git\densha-ts\work\translations_dictionary.json"
with open(dict_path, "r", encoding="utf-8") as f:
    translations = json.load(f)

# Build normalized dictionary for resilient matching
norm_translations = {}
for k, v in translations.items():
    k_clean = k.strip().replace("\u3000", " ").strip()
    norm_translations[k_clean] = v

has_jp = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')

def translate_file(in_path, out_path):
    with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    out_lines = []
    i = 0
    translated_count = 0
    missing_count = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("=>["):
            out_lines.append(line)
            i += 1

            # Collect body text lines until a header or source tag
            text_lines = []
            while (
                i < len(lines)
                and not lines[i].startswith("=>#")
                and not lines[i].startswith("=>[")
                and not lines[i].startswith("=>{")
            ):
                text_lines.append(lines[i])
                i += 1

            raw_text = "".join(text_lines).rstrip("\r\n")
            line_ending = "\n"
            if text_lines and text_lines[-1].endswith("\r\n"):
                line_ending = "\r\n"

            trans_val = raw_text
            if has_jp.search(raw_text):
                trimmed = raw_text.strip()
                normalized = trimmed.replace("\u3000", " ").strip()

                if raw_text in translations:
                    trans_val = translations[raw_text]
                    translated_count += 1
                elif trimmed in translations:
                    trans_val = translations[trimmed]
                    translated_count += 1
                elif normalized in norm_translations:
                    trans_val = norm_translations[normalized]
                    translated_count += 1
                else:
                    missing_count += 1
                    print(f"MISSING: [{raw_text}]")

            out_lines.append(trans_val + "\n\n")
        else:
            out_lines.append(line.rstrip("\r\n") + "\n")
            i += 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

    print(f"{os.path.basename(in_path)} -> {os.path.basename(out_path)}: Translated={translated_count}, Missing={missing_count}")
    return missing_count

m1 = translate_file(r"C:\git\densha-ts\work\game_all_texts.txt", r"C:\git\densha-ts\work\game_all_texts_en.txt")
m2 = translate_file(r"C:\git\densha-ts\work\datatables_locres.txt", r"C:\git\densha-ts\work\datatables_locres_en.txt")

print(f"Total missing strings: {m1 + m2}")

# Compile into binary Game.locres
locres_exe = r"C:\git\densha-ts\work\tools\UE4TextExtractor.exe"
locres_out = r"C:\git\densha-ts\work\Game.locres"
txt_in = r"C:\git\densha-ts\work\game_all_texts_en.txt"

print(f"Compiling {txt_in} -> {locres_out}...")
res = subprocess.run([locres_exe, txt_in, locres_out], capture_output=True, text=True)
if res.returncode == 0:
    print(f"Game.locres successfully compiled! Size: {os.path.getsize(locres_out)} bytes")
else:
    print(f"Error compiling Game.locres: {res.stderr}")
