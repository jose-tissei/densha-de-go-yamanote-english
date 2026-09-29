import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

raw_json_path = r"C:\git\densha-ts\work\extracted_texts.json"
out_json = r"C:\git\densha-ts\work\densha_japanese_strings.json"
out_txt = r"C:\git\densha-ts\work\densha_japanese_strings.txt"

with open(raw_json_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

hiragana = re.compile(r"[\u3040-\u309F]")
katakana = re.compile(r"[\u30A0-\u30FF]{2,}")
jp_punct = re.compile(r"[、。！？（）「」『』【】〜…・]")

def is_genuine_japanese(s):
    s = s.strip()
    if len(s) < 2:
        return False
    if hiragana.search(s) or jp_punct.search(s):
        return True
    if katakana.search(s):
        return True
    if re.fullmatch(r"[\u4E00-\u9FFF]{2,12}", s):
        is_ascii_leak = all(0x20 <= (ord(c) >> 8) <= 0x7E and 0x20 <= (ord(c) & 0xFF) <= 0x7E for c in s)
        if not is_ascii_leak:
            return True
    return False

clean_data = {}
for file, str_list in raw_data.items():
    clean_list = []
    for s in str_list:
        if is_genuine_japanese(s):
            clean_list.append(s.strip())
    if clean_list:
        clean_data[file] = sorted(list(set(clean_list)))

total_clean = sum(len(v) for v in clean_data.values())
print(f"Clean Genuine Japanese strings: {total_clean} across {len(clean_data)} files")

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=2)

with open(out_txt, "w", encoding="utf-8") as f:
    for file, strings in sorted(clean_data.items()):
        f.write("====================================================================\n")
        f.write(f"# {file} ({len(strings)} strings)\n")
        f.write("====================================================================\n")
        for s in strings:
            s_escaped = s.replace("\n", "\\n").replace("\r", "\\r")
            f.write(f"{s_escaped}\n")
        f.write("\n")

print(f"Saved cleaned strings to:\n  {out_json}\n  {out_txt}")
