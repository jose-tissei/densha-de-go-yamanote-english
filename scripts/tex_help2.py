import sys, os, re, json, shutil
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import *
import cv2
sys.stdout.reconfigure(encoding='utf-8')
SUP = 'Common/Textures/Support'
BAK = f'{W}/texout_bak/Support'
hp = json.load(open(f'{W}/ocr_help_all.json', encoding='utf-8'))
def norm(s): return re.sub(r'[\s\u3000・:：!！。、,\.\'"“”「」『』』\[\]\(\)（）@@]', '', s)

CUR = {
 '山手線': 'Yamanote Line', 'やまのてせん': 'Yamanote Line', '渋谷': 'Shibuya', 'ハイスコア': 'High Score', 'ハフコア': 'High Score',
 'ブレーキ': 'Brake', 'プレーキ': 'Brake', 'フレーキ': 'Brake', '新しくゲームを始める': 'Start a New Game', 'デイリールーレット': 'Daily Roulette',
 '高田馬場': 'Takadanobaba', '休日': 'Holiday', '平日': 'Weekday', '3区間': '3 Sections', '6区間': '6 Sections', '区間': 'Sections',
 '加速': 'Accel', 'レスティック': 'L Stick', '左ステイック': 'L Stick', 'スコア': 'Score', '運転士の道': "Driver's Path", 'ランク': 'Rank',
 'ミッションクリア': 'Clear missions!', 'クリアして解放しよう': 'Clear to unlock!', '次のミッションに進もう': 'On to the next mission!',
 '柚選が行えます': 'Roulette available.', '柚選ガ行えます': 'Roulette available.', '天気': 'Weather', '乗務を続ける': 'Continue Duty',
 '乗務をやめる': 'Quit Duty', '操作タイプシンプル': 'Control Type: Simple', '操作タイプ': 'Control Type', 'シンプル': 'Simple',
 '入カタイプ': 'Input Type', '入力タイプ': 'Input Type', 'ダイレクト': 'Direct', '指差し確認操作': 'Point & Call', '警笛を鳴らす': 'Sound Horn',
 'ワイパー': 'Wipers ON/OFF', '減光回数過多': 'Too many dims', '減光': 'Dimmer ON/OFF', '振動設定': 'Vibration', '総合スコア': 'Total Score',
 '運転記録': 'Driving Record', '辺転記録': 'Driving Record', '神田': 'Kanda', '駒込': 'Komagome', '池袋': 'Ikebukuro', '原宿': 'Harajuku',
 '有楽町': 'Yurakucho', '晴れ': 'Clear', '普通': 'Normal', '少ない': 'Few', '乗務開始': 'Start Duty', '達成度': 'Progress', '達成慶': 'Progress',
 '切り替え': 'Switch', '決定': 'Confirm', '昇格試験クリア': 'Exam Cleared', '昇格試験': 'Promotion Exam', '出発駅': 'Departure',
 'おりに入り': 'Favorites', 'お気に入り': 'Favorites', '現在速度': 'Speed', '時間帯': 'Time of Day', '非常': 'Emergency',
 '画面の明るさを調整できます': 'Adjust the screen brightness.', '画面の明るさを朗整できます': 'Adjust the screen brightness.',
 'ゲームを始めるセーブデータを選んでください': 'Select the save data to start the game with.',
 '始めるセーブデータを遥んでください': 'Select the save data to start the game with.',
 '進行状況達成度乗務回数などのプレイ情報を確認できます': 'Check play info such as progress, completion, and duty count.',
 '進行状湿達成慶乗務回数などのプレイ情報を確認できます': 'Check play info such as progress, completion, and duty count.',
 '到着時刻までの時間': 'Time Until Arrival', '剥着時刻までの時間': 'Time Until Arrival', 'すれ違い車両に減光': 'Dim for passing trains',
 '駅構内未加速': 'No accel. in station', '戸閉め後加速': 'Accel. after doors closed', 'ブレーキ込め直しなし': 'No brake re-apply',
 'セーブデータ': 'Save Data', 'セーブデーク': 'Save Data',
 '減光ONIOFF': 'Dimmer ON/OFF', '減光ONOFF': 'Dimmer ON/OFF', 'ワイパーONIOFF': 'Wipers ON/OFF', 'ワイパーONOFF': 'Wipers ON/OFF', '抽選スロット': 'Roulette Slot',
}
KEYS = sorted(CUR, key=len, reverse=True)
def lookup(t):
    nt = norm(t)
    if not nt: return None
    for k in KEYS:
        if nt == norm(k): return CUR[k]
    for k in KEYS:
        nk = norm(k)
        if len(nk) >= 2 and nk in nt and len(nk) >= 0.6 * len(nt): return CUR[k]
    return None

def retext(img, box, text, big):
    a = np.asarray(img).copy(); H, Wd = a.shape[:2]
    pad = 4 if big else 3
    x0, y0, x1, y1 = max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, Wd), min(box[3] + pad, H)
    sub = a[y0:y1, x0:x1, :3].astype(float); lum = sub.mean(axis=2)
    ring = np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]); bgc = np.median(ring, axis=0); bgl = bgc.mean()
    dist = np.abs(sub - bgc).sum(axis=2)
    m = dist > 90
    if m.sum() < 10: return img
    txt = sub[m]; tl = txt.mean(axis=1)
    light = tl.mean() > bgl
    far = txt[np.argsort(-np.abs(tl - bgl))[:max(10, len(tl) // 5)]]
    fg = tuple(int(v) for v in np.median(far, axis=0)) + (255,)
    inner = lum[~m]; bgl2 = float(np.median(inner)) if inner.size else bgl
    if abs(sum(fg[:3]) / 3 - bgl2) < 70 and not big:
        light = bgl2 < 140
        fg = (255, 255, 255, 255) if light else (20, 20, 20, 255)
    mm = np.zeros(a.shape[:2], np.uint8); mm[y0:y1, x0:x1] = m
    mm = cv2.dilate(mm, np.ones((5, 5), np.uint8))
    a[..., :3] = cv2.inpaint(np.ascontiguousarray(a[..., :3]), mm, 5, cv2.INPAINT_TELEA)
    img = Image.fromarray(a, 'RGBA'); d = ImageDraw.Draw(img)
    w = box[2] - box[0]; h = box[3] - box[1]
    maxw = int(w * (1.0 if len(text) > 18 else (1.35 if big else 1.15))); stroke = 3 if big else 0
    f, size, bb = fit_font(text, 'rodin_db' if big else 'rodin_m', maxw, int(h * (0.95 if big else 0.78)), 90)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx = (box[0] + box[2]) // 2 if big else box[0] + tw // 2 + (14 if text in ("Driver's Path", 'Daily Roulette') else 0); cy = (box[1] + box[3]) // 2
    if big and light and fg[0] > 200 and fg[2] < 140: sc = (50, 25, 5, 255)
    else: sc = (20, 20, 20, 255)
    if stroke: d.text((cx - tw // 2 - bb[0], cy - th // 2 - bb[1]), text, font=f, fill=fg, stroke_width=stroke, stroke_fill=sc)
    elif light: d.text((cx - tw // 2 - bb[0], cy - th // 2 - bb[1]), text, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(15, 40, 25, 255))
    else: d.text((cx - tw // 2 - bb[0], cy - th // 2 - bb[1]), text, font=f, fill=fg, stroke_width=1, stroke_fill=(240, 240, 240, 255))
    return img

from help_finish import white_text_clear, draw_line
def extra_112(img):
    img = white_text_clear(img, (480, 20, 1190, 74))
    draw_line(img, 'Favorites Display', (480, 24, 808, 72), 'right', stroke=3)
    draw_line(img, 'Mission Difficulty', (852, 24, 1190, 72), 'left', stroke=3)
    img = white_text_clear(img, (40, 150, 300, 198))
    draw_line(img, 'Roulette Slot', (44, 154, 296, 196), 'left', stroke=2)
    return img
def extra_028(img):
    img = retext(img, (97, 33, 240, 62), "Driver's Path", False)
    img = retext(img, (62, 91, 292, 111), 'Drive safely within the speed limit', False)
    img = retext(img, (330, 150, 386, 173), 'Gotanda', False)
    return img
EXTRAS = {'TU_SU_GameManual_112': extra_112, 'TU_SU_Control_028': extra_028}

n_ok = 0
for k, hits in hp.items():
    img = Image.open(f'{BAK}/{k}.png').convert('RGBA'); changed = 0
    for h in hits:
        t = lookup(h['t'])
        if not t: continue
        big = (h['b'][3] - h['b'][1]) >= 36
        img = retext(img, h['b'], t, big); changed += 1
    if k in EXTRAS: img = EXTRAS[k](img); changed += 1
    if changed:
        write_texture(f'{SUP}/{k}', img); n_ok += 1
        print('patched', k, changed)
print('pages', n_ok)
