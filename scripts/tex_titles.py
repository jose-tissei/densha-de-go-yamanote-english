import sys
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import *

TITLES = {
    '001': 'Driving Controls', '002': 'Menu Controls', '101': "Driver's Path", '111': 'Daily Roulette',
    '121': 'Free Run', '131': 'Arcade Mode', '141': 'VR Mode',
    '201': 'Yamanote Line', '202': 'Sobu Line', '203': 'Saikyo Line', '204': 'Ueno-Tokyo Line',
    '205': 'Keihin-Tohoku Line', '206': 'Narita Express',
    '221': 'E235 Series', '222': 'E231 Series 500 Subseries', '223': 'E233 Series', '224': 'E259 Series',
    '225': 'E217 Series', '226': '185 Series', '227': '251 Series', '228': '215 Series', '229': '189 Series',
    '252': 'Futaba',
}

def run():
    n = 0
    for k, t in TITLES.items():
        rel = f'Common/Textures/Support/TU_SU_Title_{k}'
        if rel not in IDX: print('skip', rel); continue
        img = load(rel)
        x0, y0, x1, y1 = text_bbox_alpha(img)
        h = img.size[1]
        img = clear(img, (0, 0, img.size[0], h))
        cx = img.size[0] // 2
        img, size = draw_text(img, (cx - 700, 2, cx + 700, h - 2), t, 'rodin_m', max_size=int((y1 - y0) * 1.05))
        write_texture(rel, img); n += 1
    print('titles patched', n)

if __name__ == '__main__':
    run()
