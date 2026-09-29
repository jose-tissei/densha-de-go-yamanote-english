import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

dict_path = r"C:\git\densha-ts\work\translations_dictionary.json"
with open(dict_path, "r", encoding="utf-8") as f:
    translations = json.load(f)

has_jp = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')

def translate_file(in_path, out_path):
    with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    entries = content.split("=>[")
    header = entries[0]
    out_parts = [header]

    translated_count = 0
    missing_count = 0

    for e in entries[1:]:
        header_line, text_body = e.split("\n", 1)
        # Separate source text from any following =>#
        lines = text_body.split("\n=>#")
        raw_val = lines[0].strip("\r\n")
        following = ("\n=>#" + lines[1]) if len(lines) > 1 else ""

        trans_val = raw_val
        if has_jp.search(raw_val):
            if raw_val in translations:
                trans_val = translations[raw_val]
                translated_count += 1
            else:
                # Try trimmed / cleaned
                trimmed = raw_val.strip()
                if trimmed in translations:
                    trans_val = translations[trimmed]
                    translated_count += 1
                else:
                    missing_count += 1
                    print(f"MISSING: [{raw_val}]")

        out_parts.append(f"{header_line}\n{trans_val}{following}")

    result = "=>[".join(out_parts)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"{os.path.basename(in_path)} -> {os.path.basename(out_path)}: Translated={translated_count}, Missing={missing_count}")
    return missing_count

m1 = translate_file(r"C:\git\densha-ts\work\game_all_texts.txt", r"C:\git\densha-ts\work\game_all_texts_en.txt")
m2 = translate_file(r"C:\git\densha-ts\work\datatables_locres.txt", r"C:\git\densha-ts\work\datatables_locres_en.txt")

print(f"Total missing strings: {m1 + m2}")
