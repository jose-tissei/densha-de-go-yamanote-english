import sys, os, json
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import load, write_texture, font, fit_font, draw_text, clear

W = r'C:\git\densha-ts\work'

def patch_tutorial_mascon():
    rel = 'InGame/Tutorial/Textures/TU_Tutorial_mascon'
    im = load(rel)
    d = ImageDraw.Draw(im)
    # Clear "現在速度"
    d.rectangle([270, 368, 368, 400], fill=(20, 25, 20, 255))
    im, _ = draw_text(im, (270, 368, 368, 400), 'Current Speed', fontname='bold',
                      color=(255, 255, 255, 255), max_size=14, stroke=1)
    # Clear "制限速度"
    d.rectangle([600, 226, 654, 250], fill=(25, 30, 25, 255))
    im, _ = draw_text(im, (600, 226, 654, 250), 'Limit', fontname='bold',
                      color=(255, 255, 255, 255), max_size=14, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def patch_tutorial_nokorikyori():
    rel = 'InGame/Tutorial/Textures/TU_Tutorial_nokorikyori'
    im = load(rel)
    d = ImageDraw.Draw(im)
    # Clear "到着時刻まで"
    d.rectangle([275, 455, 360, 485], fill=(20, 20, 20, 255))
    im, _ = draw_text(im, (275, 455, 360, 485), 'To Arrival', fontname='bold',
                      color=(255, 255, 255, 255), max_size=14, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def patch_tutorial_score():
    rel = 'InGame/Tutorial/Textures/TU_Tutorial_score'
    im = load(rel)
    d = ImageDraw.Draw(im)
    # Service Horn
    d.rectangle([800, 270, 995, 320], fill=(10, 10, 10, 255))
    im, _ = draw_text(im, (800, 270, 995, 320), 'Service Horn', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=24, stroke=2)
    # Ignore Speed (1)
    d.rectangle([735, 525, 998, 582], fill=(160, 25, 25, 255))
    im, _ = draw_text(im, (735, 525, 998, 582), 'Ignore Speed', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=24, stroke=2)
    # Ignore Speed (2)
    d.rectangle([735, 672, 998, 726], fill=(160, 25, 25, 255))
    im, _ = draw_text(im, (735, 672, 998, 726), 'Ignore Speed', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=24, stroke=2)
    # Mission Clear Target
    d.rectangle([710, 840, 900, 880], fill=(15, 15, 15, 255))
    im, _ = draw_text(im, (710, 840, 900, 880), 'Clear Target', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=18, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def patch_tutorial_score_02():
    rel = 'InGame/Tutorial/Textures/TU_Tutorial_score_02'
    im = load(rel)
    d = ImageDraw.Draw(im)
    # Ignore Speed boxes
    d.rectangle([355, 145, 502, 178], fill=(170, 40, 40, 255))
    im, _ = draw_text(im, (355, 145, 502, 178), 'Ignore Speed', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=16, stroke=1)
    d.rectangle([355, 230, 502, 262], fill=(170, 40, 40, 255))
    im, _ = draw_text(im, (355, 230, 502, 262), 'Ignore Speed', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=16, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def main():
    patch_tutorial_mascon()
    patch_tutorial_nokorikyori()
    patch_tutorial_score()
    patch_tutorial_score_02()

    verified_path = f'{W}/jp_textures_verified.json'
    v = json.load(open(verified_path, encoding='utf-8'))

    patched_keys = [
        'InGame/Tutorial/Textures/TU_Tutorial_mascon',
        'InGame/Tutorial/Textures/TU_Tutorial_nokorikyori',
        'InGame/Tutorial/Textures/TU_Tutorial_score',
        'InGame/Tutorial/Textures/TU_Tutorial_score_02',
    ]
    for k in patched_keys:
        if k in v:
            v[k]['patched'] = True

    false_positives = [
        'InGame/Tutorial/Textures/TU_Tutorial_button',
        'InGame/Tutorial/Textures/TU_Tutorial_stop',
    ]
    for k in false_positives:
        if k in v:
            v[k]['task'] = 'FalsePositive'
            v[k]['patched'] = True

    with open(verified_path, 'w', encoding='utf-8') as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

    print('Successfully updated jp_textures_verified.json! All T7 tutorial textures processed.')

if __name__ == '__main__':
    main()
