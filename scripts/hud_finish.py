import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import load, write_texture, font, fit_font, draw_text, clear

W = r'C:\git\densha-ts\work'

def patch_ymt103_limit():
    rel = 'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_LimitSpeedBase'
    im = load(rel)
    # Clear Japanese text
    im = clear(im, (15, 0, 115, 28), rgb=(0, 0, 0))
    # Draw English text
    im, _ = draw_text(im, (12, 0, 118, 28), 'Speed Limit', fontname='bold', color=(255, 250, 240, 255), max_size=18, stroke=2)
    write_texture(rel, im)
    print('Patched', rel)

def patch_ymt103_speed():
    rel = 'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_Speedometer'
    im = load(rel)
    im = clear(im, (695, 412, 885, 458), rgb=(30, 30, 30))
    im, _ = draw_text(im, (695, 412, 885, 458), 'Current Speed', fontname='bold', color=(255, 250, 240, 255), max_size=24, stroke=2)
    write_texture(rel, im)
    print('Patched', rel)

def patch_ymt205_speed():
    rel = 'InGame/HUD/YMT205/Textures/TU_HUD_YMT205_Speedometer'
    im = load(rel)
    im = clear(im, (390, 85, 505, 130), rgb=(20, 20, 20))
    im, _ = draw_text(im, (390, 85, 505, 130), 'Speed Limit', fontname='bold', color=(255, 250, 240, 255), max_size=20, stroke=2)
    im = clear(im, (330, 465, 440, 510), rgb=(20, 20, 20))
    im, _ = draw_text(im, (330, 465, 440, 510), 'Current Speed', fontname='bold', color=(255, 250, 240, 255), max_size=20, stroke=2)
    write_texture(rel, im)
    print('Patched', rel)

def patch_ymt205_dest():
    rel = 'InGame/HUD/YMT205/Textures/TU_HUD_YMT205_destination'
    im = load(rel)
    # Fill green band over the text
    d = ImageDraw.Draw(im)
    d.rectangle([255, 172, 355, 218], fill=(138, 203, 76, 255))
    im, _ = draw_text(im, (255, 172, 355, 218), 'Ridership', fontname='bold', color=(255, 255, 255, 255), max_size=22, stroke=2)
    write_texture(rel, im)
    print('Patched', rel)

def patch_ymt103_kpa():
    rel = 'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_KpaMeter'
    im = load(rel)
    d = ImageDraw.Draw(im)
    d.rectangle([195, 122, 305, 156], fill=(232, 206, 137, 255))
    im, _ = draw_text(im, (195, 122, 305, 156), 'Air Pressure', fontname='bold', color=(40, 35, 30, 255), max_size=18)
    write_texture(rel, im)
    print('Patched', rel)

def patch_ymt103_em():
    rel = 'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_Gauge_Em'
    im = load(rel)
    d = ImageDraw.Draw(im)
    d.rectangle([14, 25, 52, 95], fill=(215, 20, 20, 255))
    # Draw EMG vertically
    f = font('bold', 20)
    d.text((22, 28), 'E', font=f, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(50, 0, 0, 255))
    d.text((20, 50), 'M', font=f, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(50, 0, 0, 255))
    d.text((22, 72), 'G', font=f, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(50, 0, 0, 255))
    write_texture(rel, im)
    print('Patched', rel)

def patch_ymt231_em(name):
    rel = f'InGame/HUD/YMT231/Textures/{name}'
    im = load(rel)
    im = clear(im, (84, 14, 124, 66), rgb=(30, 30, 30))
    d = ImageDraw.Draw(im)
    d.rectangle([84, 14, 124, 66], fill=(35, 35, 35, 255))
    im, _ = draw_text(im, (84, 14, 124, 66), 'EMG', fontname='bold', color=(255, 255, 255, 255), max_size=22, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def patch_ske233_em():
    rel = 'InGame/HUD/SKE233_PS4/Textures/TU_HUD_SKE233_Gauge_Black'
    im = load(rel)
    im = clear(im, (15, 0, 75, 26), rgb=(30, 30, 30))
    d = ImageDraw.Draw(im)
    d.rectangle([15, 0, 75, 26], fill=(35, 35, 35, 255))
    im, _ = draw_text(im, (15, 0, 75, 26), 'EMG', fontname='bold', color=(255, 255, 255, 255), max_size=18, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def main():
    patch_ymt103_limit()
    patch_ymt103_speed()
    patch_ymt205_speed()
    patch_ymt205_dest()
    patch_ymt103_kpa()
    patch_ymt103_em()
    patch_ymt231_em('TU_HUD_YMT231_Gauge_Blank')
    patch_ymt231_em('TU_HUD_YMT231_Gauge_SBlank')
    patch_ske233_em()

    # Update verification list
    verified_path = f'{W}/jp_textures_verified.json'
    v = json.load(open(verified_path, encoding='utf-8'))
    
    patched_keys = [
        'InGame/HUD/SKE233/Textures/TU_HUD_SKE233_difficulty_easy',
        'InGame/HUD/SKE233/Textures/TU_HUD_SKE233_difficulty_normal',
        'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_LimitSpeedBase',
        'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_Speedometer',
        'InGame/HUD/YMT205/Textures/TU_HUD_YMT205_Speedometer',
        'InGame/HUD/YMT205/Textures/TU_HUD_YMT205_destination',
        'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_KpaMeter',
        'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_Gauge_Em',
        'InGame/HUD/YMT231/Textures/TU_HUD_YMT231_Gauge_Blank',
        'InGame/HUD/YMT231/Textures/TU_HUD_YMT231_Gauge_SBlank',
        'InGame/HUD/SKE233_PS4/Textures/TU_HUD_SKE233_Gauge_Black'
    ]
    false_positives = [
        'InGame/HUD/NEX259/Textures/TU_HUD_NEX259_Base',
        'InGame/HUD/NEX259/Textures/TU_HUD_NEX259_Speedometer',
        'InGame/HUD/NEX259/Textures/TU_HUD_NEX259_Text_M',
        'InGame/HUD/NEX259/Textures/TU_HUD_NEX259_standard_p5',
        'InGame/HUD/SKE233_PS4/Textures/TU_HUD_SKE233_Gauge_SimpleB',
        'InGame/HUD/SKE233_PS4/Textures/TU_HUD_SKE233_standard_p5',
        'InGame/HUD/UTL233_PS4/Textures/TU_HUD_UTL233_Base',
        'InGame/HUD/YMT103/Textures/TU_HUD_YMT103_BHundleCap'
    ]

    for k in patched_keys:
        if k in v:
            v[k]['patched'] = True

    for k in false_positives:
        if k in v:
            v[k]['task'] = 'FalsePositive'
            v[k]['patched'] = True

    with open(verified_path, 'w', encoding='utf-8') as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print('Updated jp_textures_verified.json! All 19 T5 textures processed.')

if __name__ == '__main__':
    main()
