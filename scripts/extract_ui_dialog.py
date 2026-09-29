import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\git\densha-ts\work\densha_japanese_strings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hiragana = re.compile(r"[\u3040-\u309F]")
katakana = re.compile(r"[\u30A0-\u30FF]{2,}")
jp_punct = re.compile(r"[、。！？（）「」『』【】〜…・]")

ui_and_tables = {}
for file, strings in data.items():
    if "DataTable" in file or "WI_" in file or "Widget" in file or "Dialog" in file or "Menu" in file:
        real_ui_strings = []
        for s in strings:
            if hiragana.search(s) or katakana.search(s) or jp_punct.search(s):
                real_ui_strings.append(s)
            elif len(s) >= 2 and not any(0x4E00 <= ord(c) <= 0x9FFF and ((ord(c) >> 8) in range(0x4F, 0x60)) for c in s):
                real_ui_strings.append(s)
        if real_ui_strings:
            ui_and_tables[file] = real_ui_strings

print(f"UI and DataTable files: {len(ui_and_tables)}")
total_ui = sum(len(v) for v in ui_and_tables.values())
print(f"Total authentic UI & Game strings: {total_ui}")

out_file = r"C:\git\densha-ts\work\densha_ui_and_dialog_strings.txt"
with open(out_file, "w", encoding="utf-8") as f:
    for file, str_list in sorted(ui_and_tables.items()):
        f.write("====================================================================\n")
        f.write(f"# {file} ({len(str_list)} strings)\n")
        f.write("====================================================================\n")
        for s in str_list:
            s_clean = s.replace("\n", "\\n").replace("\r", "\\r")
            f.write(f"{s_clean}\n")
        f.write("\n")
print(f"Written to {out_file}")
