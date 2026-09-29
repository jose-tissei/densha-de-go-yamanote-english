import os
import sys
import json
import re
import time
import torch

sys.stdout.reconfigure(encoding='utf-8')
os.environ['HF_HOME'] = r'C:\git\densha-ts\work\hf_cache'

dict_path = r"C:\git\densha-ts\work\translations_dictionary.json"
strings_path = r"C:\git\densha-ts\work\strings_to_translate.json"

with open(strings_path, "r", encoding="utf-8") as f:
    strings_to_translate = json.load(f)

if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        translations = json.load(f)
else:
    translations = {}

# Comprehensive Railway & Game Glossary
GLOSSARY = {
    # Core Mechanics & Driving
    "マスコン": "Master Controller",
    "ブレーキ": "Brake",
    "警笛": "Horn",
    "減光": "Dim Headlights",
    "定速帯": "Constant Speed Zone",
    "制限速度": "Speed Limit",
    "停車位置": "Stopping Position",
    "停車案内": "Stopping Guidance",
    "停車自動": "Auto-Stop",
    "なぞり自動": "Auto-Trace",
    "タッチ自動": "Auto-Touch",
    "警笛減光自動": "Auto Horn & Dimmer",
    "なぞり案内": "Trace Guidance",
    "タッチ案内": "Touch Guidance",
    "警笛減光案内": "Horn & Dimmer Guidance",
    "出発合図": "Departure Signal",
    "出発進行": "Departure All Clear",
    "進行": "Proceed (Green)",
    "注意": "Caution (Yellow)",
    "警戒": "Warning (Yellow/Yellow)",
    "停止": "Stop (Red)",
    "場内": "Home Signal",
    "出発": "Departure Signal",
    "閉塞": "Block Signal",
    "本線出発": "Main Line Departure",
    "本線場内": "Main Line Home",
    "第1閉塞": "1st Block Signal",
    "第2閉塞": "2nd Block Signal",
    "第3閉塞": "3rd Block Signal",
    "第4閉塞": "4th Block Signal",
    "第5閉塞": "5th Block Signal",
    "第6閉塞": "6th Block Signal",
    "第7閉塞": "7th Block Signal",
    "第8閉塞": "8th Block Signal",
    "Gセンサー超過": "G-Sensor Exceeded",
    "Gセンサー遵守": "G-Sensor Complied",
    "すれ違い車両に減光": "Dimming for Passing Train",
    "出発合図後加速": "Acceleration After Departure Signal",
    "定速帯走行": "Constant Speed Zone Running",
    "戸締め点灯": "Door Indicator Lit",
    "戸じめ点灯": "Door Indicator Lit",
    "戸締め確認": "Door Closure Checked",
    "指差喚呼": "Point and Call",
    "安全確認": "Safety Check",
    "ブレーキテスト": "Brake Test",
    "非常ブレーキ": "Emergency Brake",
    "常用ブレーキ": "Service Brake",
    "力行": "Acceleration",
    "惰行": "Coasting",

    # Difficulty & Modes
    "難易度選択": "Select Difficulty",
    "難易度": "Difficulty",
    "難易度 【初級】": "Difficulty [Beginner]",
    "難易度 【中級】": "Difficulty [Intermediate]",
    "難易度 【上級】": "Difficulty [Advanced]",
    "初級": "Beginner",
    "中級": "Intermediate",
    "上級": "Advanced",
    "特級": "Expert",
    "プロフェッショナル": "Professional",
    "リアルモード": "Real Mode",
    "アーケードモード": "Arcade Mode",
    "おうちでGO!!": "At-Home GO!!",
    "VRモード": "VR Mode",
    "オプション": "Options",
    "ミッション選択": "Select Mission",
    "ミッション": "Mission",
    "ポイント購入": "Purchase Points",
    "乗車率": "Passenger Congestion",
    "極少": "Very Low",
    "少ない": "Low",
    "普通": "Normal",
    "多い": "High",
    "超満員": "Overcrowded",
    "変動": "Fluctuating",
    "天気": "Weather",
    "晴れ": "Clear",
    "曇り": "Cloudy",
    "雨": "Rain",
    "雪": "Snow",
    "朝": "Morning",
    "昼": "Day",
    "夕": "Evening",
    "夜": "Night",
    "時間": "Time",
    "上り": "Inbound",
    "下り": "Outbound",
    "内回り": "Inner Loop",
    "外回り": "Outer Loop",

    # Yamanote Stations
    "東京": "Tokyo",
    "有楽町": "Yurakucho",
    "新橋": "Shimbashi",
    "浜松町": "Hamamatsucho",
    "田町": "Tamachi",
    "高輪ゲートウェイ": "Takanawa Gateway",
    "品川": "Shinagawa",
    "大崎": "Osaki",
    "五反田": "Gotanda",
    "目黒": "Meguro",
    "恵比寿": "Ebisu",
    "渋谷": "Shibuya",
    "原宿": "Harajuku",
    "代々木": "Yoyogi",
    "新宿": "Shinjuku",
    "新大久保": "Shin-Okubo",
    "高田馬場": "Takadanobaba",
    "目白": "Mejiro",
    "池袋": "Ikebukuro",
    "大塚": "Otsuka",
    "巣鴨": "Sugamo",
    "駒込": "Komagome",
    "田端": "Tabata",
    "西日暮里": "Nishi-Nippori",
    "日暮里": "Nippori",
    "鶯谷": "Uguisudani",
    "上野": "Ueno",
    "御徒町": "Okachimachi",
    "秋葉原": "Akihabara",
    "神田": "Kanda",

    # Osaka / Kansai / Other Stations
    "大阪": "Osaka",
    "新大阪": "Shin-Osaka",
    "京都": "Kyoto",
    "名古屋": "Nagoya",
    "金山": "Kanayama",
    "熱田": "Atsuta",
    "尼崎": "Amagasaki",
    "甲子園": "Koshien",
    "武庫川": "Mukogawa",
    "鳴尾": "Naruo",
    "今津": "Imazu",
    "西宮": "Nishinomiya",
    "香櫨園": "Koruen",
    "打出": "Uchide",
    "出屋敷": "Deyashiki",
    "尼崎センタープール前": "Amagasaki Center Pool-mae",
    "久寿川": "Kusugawa",
    "大物": "Daimotsu",
    "野田": "Noda",
    "福島": "Fukushima",
    "天満": "Temma",
    "桜ノ宮": "Sakuranomiya",
    "京橋": "Kyobashi",
    "大阪城公園": "Osakajokoen",
    "森ノ宮": "Morinomiya",
    "玉造": "Tamatsukuri",
    "鶴橋": "Tsuruhashi",
    "桃谷": "Momodani",
    "寺田町": "Teradacho",
    "天王寺": "Tennoji",
    "新今宮": "Shin-Imamiya",
    "今宮": "Imamiya",
    "芦原橋": "Ashiharabashi",
    "大正": "Taisho",
    "弁天町": "Bentencho",
    "西九条": "Nishikujo",
    "千種": "Chikusa",
    "大曽根": "Ozone",
    "鶴舞": "Tsurumai",
    "飯田橋": "Iidabashi",
    "錦糸町": "Kinshicho",
    "両国": "Ryogoku",

    # Lines & Trains
    "山手線": "Yamanote Line",
    "京浜東北線": "Keihin-Tohoku Line",
    "東海道線": "Tokaido Line",
    "中央線": "Chuo Line",
    "総武線": "Sobu Line",
    "埼京線": "Saikyo Line",
    "湘南新宿ライン": "Shonan-Shinjuku Line",
    "上野東京ライン": "Ueno-Tokyo Line",
    "成田エクスプレス": "Narita Express",

    # UI Buttons & Menus
    "はい": "Yes",
    "いいえ": "No",
    "決定": "Confirm",
    "戻る": "Back",
    "キャンセル": "Cancel",
    "次へ": "Next",
    "閉じる": "Close",
    "リトライ": "Retry",
    "ポーズ": "Pause",
    "タイトルへ": "Title Screen",
    "セーブ": "Save",
    "ロード": "Load",
    "オートセーブ": "Auto-Save",
    "クリア": "Clear",
    "合格": "Passed",
    "不合格": "Failed",
    "運転評価": "Driving Evaluation",
    "総合評価": "Total Evaluation",
    "スコア": "Score",
    "ボーナス": "Bonus",
    "減点": "Penalty",
    "加点": "Bonus Points",
    "定通": "On-Time Pass",
    "定時": "On-Time",
    "早着": "Early Arrival",
    "延着": "Delay",
    "停止位置誤差": "Stopping Accuracy",
    "スコア集計中": "Calculating Score...",
    "運転お疲れ様でした": "Thank you for driving!",
    "GOバッジ": "GO Badge",
    "GOワッペン": "GO Emblem",
    "GOマイスターランク": "GO Meister Rank",
    "初心者セット・ゴールド": "Beginner Set - Gold",
    "初心者セット・シルバー": "Beginner Set - Silver",
    "初心者セット・ブロンズ": "Beginner Set - Bronze",
    "~ミッション失敗時の会話~": "~Mission Failed Dialogue~",
    "~ミッション成功時の会話~": "~Mission Success Dialogue~",
    "~導入部分の会話~": "~Mission Intro Dialogue~",
}

for jp, en in GLOSSARY.items():
    translations[jp] = en

# Pattern matching rules
pattern_rules = [
    (re.compile(r"^(\d+)番線 ドアが閉まります。ご注意ください。$"), r"Track \1 doors are closing. Please stand clear."),
    (re.compile(r"^(.+) (.+) ご乗車ありがとうございます。$"), r"Now arriving at \1, \1. Thank you for riding."),
    (re.compile(r"^難易度 【(.+)】 をクリアすると\\n選択可能になります。$"), r"Unlocked by clearing [\1] difficulty."),
    (re.compile(r"^難易度 【(.+)】 をクリアすると\n選択可能になります。$"), r"Unlocked by clearing [\1] difficulty."),
    (re.compile(r"^【上級】をクリアするか、【リアルモード解放権】を\\nマイページで購入すると切り替えが可能になります。$"),
     r"Available after clearing [Advanced] or by\npurchasing [Real Mode Access] in My Page."),
    (re.compile(r"^【上級】をクリアすると切り替えが可能になります。$"), r"Available after clearing [Advanced]."),
    (re.compile(r"^GOバッジの効果が\\n有効になりました。$"), r"GO Badge effects are now active."),
    (re.compile(r"^GOバッジの効果が\n有効になりました。$"), r"GO Badge effects are now active."),
    (re.compile(r"^GOワッペンが\\n表示されなくなりました。$"), r"GO Emblem is now hidden."),
    (re.compile(r"^GOワッペンが\\n表示されるようになりました。$"), r"GO Emblem is now displayed."),
    (re.compile(r"^プレイ時間はおよそ(\d+)分。(\d+)区間を走行するミッションがプレイできます。$"),
     r"Estimated play time: ~\1 min. Drive across \2 sections."),
    (re.compile(r"^プレイ時間はおよそ(\d+)分。"), r"Estimated play time: ~\1 min. "),
    (re.compile(r"^(\\n)?もう少し速度を上げましょう$"), r"\1Increase speed slightly."),
    (re.compile(r"^(\\n)?もう少し速度を落としましょう$"), r"\1Reduce speed slightly."),
    (re.compile(r"^(\\n)?もっと速度を上げてください$"), r"\1Please increase speed more."),
    (re.compile(r"^(\\n)?速度を落としましょう$"), r"\1Please reduce speed."),
    (re.compile(r"^定速帯終了まで$"), r"Until constant speed zone ends"),
    (re.compile(r"^制限速度まで$"), r"Until speed limit"),
    (re.compile(r"^まで$"), r"Until"),
]

for s in strings_to_translate:
    if s not in translations:
        for pat, repl in pattern_rules:
            if pat.search(s):
                translations[s] = pat.sub(repl, s)
                break

print(f"Glossary + Rules applied! Total translated: {len(translations)} / {len(strings_to_translate)}", flush=True)

# Neural Model Translation for remaining strings
remaining = [s for s in strings_to_translate if s not in translations]
print(f"Remaining strings to translate via MarianMT: {len(remaining)}", flush=True)

if remaining:
    from transformers import MarianMTModel, MarianTokenizer
    model_name = "Helsinki-NLP/opus-mt-ja-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name, use_safetensors=True).cuda()
    model.eval()

    BATCH_SIZE = 64
    for i in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[i : i + BATCH_SIZE]
        processed_batch = [s.replace("\r\n", " __BR__ ").replace("\n", " __BR__ ") for s in batch]
        inputs = tokenizer(processed_batch, return_tensors="pt", padding=True, truncation=True, max_length=128).to("cuda")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=80, num_beams=1)
        decoded = [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]

        for orig, trans in zip(batch, decoded):
            clean_trans = trans.replace("__BR__", "\n").replace(" __BR__ ", "\n").replace(" __br__ ", "\n")
            clean_trans = re.sub(r" +", " ", clean_trans).strip()
            translations[orig] = clean_trans

        print(f"Progress: {min(i + BATCH_SIZE, len(remaining))} / {len(remaining)} translated...", flush=True)

with open(dict_path, "w", encoding="utf-8") as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"All translations finished! Total translations in dictionary: {len(translations)}", flush=True)
