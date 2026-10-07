import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import load, write_texture, font, fit_font, draw_text, clear

W = r'C:\git\densha-ts\work'

def patch_title_start():
    # 00: Unselected state
    rel0 = 'OutGame/Title/TitleTop_GameStartText_00'
    im0 = load(rel0)
    im0 = clear(im0, (0, 0, 1024, 128))
    # Green Yamanote text with dark outline
    d0 = ImageDraw.Draw(im0)
    f0 = font('rodin_eb', 70)
    bb0 = d0.textbbox((0, 0), 'GAME START', font=f0)
    tw0, th0 = bb0[2] - bb0[0], bb0[3] - bb0[1]
    x0 = (1024 - tw0) // 2 - bb0[0]
    y0 = (128 - th0) // 2 - bb0[1]
    d0.text((x0, y0), 'GAME START', font=f0, fill=(153, 215, 68, 255),
            stroke_width=4, stroke_fill=(20, 45, 10, 255))
    write_texture(rel0, im0)
    print('Patched', rel0)

    # 01: Selected / Glowing state
    rel1 = 'OutGame/Title/TitleTop_GameStartText_01'
    im1 = load(rel1)
    im1 = clear(im1, (0, 0, 1024, 128))
    d1 = ImageDraw.Draw(im1)
    f1 = font('rodin_eb', 70)
    bb1 = d1.textbbox((0, 0), 'GAME START', font=f1)
    tw1, th1 = bb1[2] - bb1[0], bb1[3] - bb1[1]
    x1 = (1024 - tw1) // 2 - bb1[0]
    y1 = (128 - th1) // 2 - bb1[1]
    # Lighter green text with glowing green outline
    d1.text((x1, y1), 'GAME START', font=f1, fill=(230, 255, 170, 255),
            stroke_width=5, stroke_fill=(70, 180, 25, 255))
    write_texture(rel1, im1)
    print('Patched', rel1)

def patch_main_menu_header():
    rel = 'OutGame/MeinMenu/Textures/TU_MM_Header_02'
    im = load(rel)
    # Clear "メインメニュー" at x: 35..215, y: 45..90
    d = ImageDraw.Draw(im)
    d.rectangle([35, 45, 215, 90], fill=(22, 28, 22, 255))
    im, _ = draw_text(im, (38, 48, 212, 88), 'MAIN MENU', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=28, stroke=2)
    write_texture(rel, im)
    print('Patched', rel)

def patch_save_progress():
    # off
    rel_off = 'OutGame/SaveData/Textures/tu_save_progress_text_off'
    im_off = load(rel_off)
    im_off = clear(im_off, (0, 0, 512, 64))
    im_off, _ = draw_text(im_off, (20, 5, 492, 58), "Driver's Path Progress",
                          fontname='rodin_eb', color=(147, 147, 147, 255), max_size=26, stroke=2)
    write_texture(rel_off, im_off)
    print('Patched', rel_off)

    # on
    rel_on = 'OutGame/SaveData/Textures/tu_save_progress_text_on'
    im_on = load(rel_on)
    im_on = clear(im_on, (0, 0, 512, 64))
    im_on, _ = draw_text(im_on, (20, 5, 492, 58), "Driver's Path Progress",
                         fontname='rodin_eb', color=(154, 222, 17, 255), max_size=26, stroke=2)
    write_texture(rel_on, im_on)
    print('Patched', rel_on)

def patch_mission_gauge():
    rel = 'InGame/Common/Textures/TU_MG_GaugeBG'
    im = load(rel)
    d = ImageDraw.Draw(im)
    d.rectangle([420, 8, 590, 36], fill=(25, 25, 25, 255))
    im, _ = draw_text(im, (422, 8, 588, 36), 'MISSION GAUGE', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=16, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def patch_mission_result():
    # Arrival Time Early (01)
    rel1 = 'InGame/MissionResult/Textures/TU_MR_TextArrivalTime01'
    im1 = load(rel1)
    im1 = clear(im1, (20, 55, 150, 140))
    im1, _ = draw_text(im1, (20, 58, 148, 92), 'Arrival', fontname='bold',
                       color=(255, 255, 255, 255), max_size=18, stroke=2)
    im1, _ = draw_text(im1, (20, 96, 148, 134), 'Ahead', fontname='bold',
                       color=(255, 255, 255, 255), max_size=18, stroke=2)
    write_texture(rel1, im1)
    print('Patched', rel1)

    # Arrival Time Late (02)
    rel2 = 'InGame/MissionResult/Textures/TU_MR_TextArrivalTime02'
    im2 = load(rel2)
    im2 = clear(im2, (20, 55, 150, 140))
    im2, _ = draw_text(im2, (20, 58, 148, 92), 'Arrival', fontname='bold',
                       color=(255, 255, 255, 255), max_size=18, stroke=2)
    im2, _ = draw_text(im2, (20, 96, 148, 134), 'Late', fontname='bold',
                       color=(255, 255, 255, 255), max_size=18, stroke=2)
    write_texture(rel2, im2)
    print('Patched', rel2)

    # Delay
    rel_del = 'InGame/MissionResult/Textures/TU_MR_TextDelay'
    im_del = load(rel_del)
    im_del = clear(im_del, (20, 55, 145, 135))
    im_del, _ = draw_text(im_del, (25, 65, 140, 125), 'Delay', fontname='bold',
                          color=(255, 255, 255, 255), max_size=24, stroke=2)
    write_texture(rel_del, im_del)
    print('Patched', rel_del)

    # Second
    rel_sec = 'InGame/MissionResult/Textures/TU_MR_TextSecond'
    im_sec = load(rel_sec)
    im_sec = clear(im_sec, (10, 10, 90, 90))
    im_sec, _ = draw_text(im_sec, (15, 15, 85, 85), 's', fontname='bold',
                          color=(255, 255, 255, 255), max_size=32, stroke=2)
    write_texture(rel_sec, im_sec)
    print('Patched', rel_sec)

def patch_total_result():
    # Banner 01
    rel_b = 'InGame/TotalResult/Textures/TU_TotalResult_banner01'
    im_b = load(rel_b)
    # Clear & draw Difficulty, Weather, Ridership
    d_b = ImageDraw.Draw(im_b)
    d_b.rectangle([815, 35, 945, 95], fill=(30, 30, 30, 255))
    im_b, _ = draw_text(im_b, (815, 38, 945, 92), 'Difficulty', fontname='rodin_eb',
                        color=(255, 255, 255, 255), max_size=20, stroke=1)
    d_b.rectangle([1105, 35, 1205, 95], fill=(30, 30, 30, 255))
    im_b, _ = draw_text(im_b, (1105, 38, 1205, 92), 'Weather', fontname='rodin_eb',
                        color=(255, 255, 255, 255), max_size=20, stroke=1)
    d_b.rectangle([1295, 35, 1425, 95], fill=(30, 30, 30, 255))
    im_b, _ = draw_text(im_b, (1295, 38, 1425, 92), 'Ridership', fontname='rodin_eb',
                        color=(255, 255, 255, 255), max_size=20, stroke=1)
    write_texture(rel_b, im_b)
    print('Patched', rel_b)

    # Window 01
    rel_w = 'InGame/TotalResult/Textures/TU_TotalResult_window01'
    im_w = load(rel_w)
    d_w = ImageDraw.Draw(im_w)
    d_w.rectangle([360, 0, 540, 62], fill=(25, 25, 25, 255))
    im_w, _ = draw_text(im_w, (365, 2, 535, 60), 'Score', fontname='rodin_eb',
                        color=(255, 255, 255, 255), max_size=24, stroke=1)
    d_w.rectangle([660, 0, 845, 62], fill=(25, 25, 25, 255))
    im_w, _ = draw_text(im_w, (665, 2, 840, 60), 'High Score', fontname='rodin_eb',
                        color=(255, 255, 255, 255), max_size=24, stroke=1)
    d_w.rectangle([870, 0, 990, 62], fill=(25, 25, 25, 255))
    im_w, _ = draw_text(im_w, (875, 2, 985, 60), 'Rank', fontname='rodin_eb',
                        color=(255, 255, 255, 255), max_size=24, stroke=1)
    write_texture(rel_w, im_w)
    print('Patched', rel_w)

def patch_free_mode():
    # Simple badges
    badges = [
        ('OutGame/FreeMode/Textures/TU_FM_k_1_02', 'Light'),
        ('OutGame/FreeMode/Textures/TU_FM_k_2_01', 'Clear'),
        ('OutGame/FreeMode/Textures/TU_FM_k_2_02', 'Rain'),
        ('OutGame/FreeMode/Textures/TU_FM_k_2_03', 'Snow'),
        ('OutGame/FreeMode/Textures/TU_FM_k_3_01', 'Morning'),
        ('OutGame/FreeMode/Textures/TU_FM_k_3_02', 'Day'),
    ]
    for rel, text in badges:
        im = load(rel)
        # Clear middle band where Japanese kanji is centered
        d = ImageDraw.Draw(im)
        # Find dark region or clear text
        im, _ = draw_text(im, (30, 80, 480, 180), text, fontname='rodin_eb',
                          color=(255, 255, 255, 255), max_size=36, stroke=3)
        write_texture(rel, im)
        print('Patched', rel)

    # TU_FM_right_bg_base (512x1024)
    rel_bg = 'OutGame/FreeMode/Textures/TU_FM_right_bg_base'
    im_bg = load(rel_bg)
    d_bg = ImageDraw.Draw(im_bg)
    fields = [
        ([75, 25, 230, 80], 'Train Model', (247, 247, 247, 255)),
        ([75, 225, 230, 280], 'Settings', (247, 247, 247, 255)),
        ([75, 310, 230, 368], 'Departure', (247, 247, 247, 255)),
        ([75, 440, 230, 495], 'Arrival', (246, 246, 246, 255)),
        ([75, 570, 290, 630], 'Play Time', (246, 246, 246, 255)),
        ([75, 715, 210, 768], 'Time of Day', (244, 244, 244, 255)),
        ([75, 790, 185, 842], 'Weather', (240, 240, 240, 255)),
        ([275, 788, 415, 842], 'Ridership', (240, 240, 240, 255)),
    ]
    for box, txt, bg in fields:
        d_bg.rectangle(box, fill=bg)
        im_bg, _ = draw_text(im_bg, tuple(box), txt, fontname='rodin_eb',
                             color=(35, 35, 35, 255), max_size=22)
    write_texture(rel_bg, im_bg)
    print('Patched', rel_bg)

    # TU_FM_verification_card
    rel_card = 'OutGame/FreeMode/Textures/TU_FM_verification_card'
    im_card = load(rel_card)
    d_card = ImageDraw.Draw(im_card)
    d_card.rectangle([470, 372, 570, 415], fill=(30, 30, 30, 255))
    im_card, _ = draw_text(im_card, (470, 372, 570, 415), 'Ridership', fontname='rodin_eb',
                           color=(255, 255, 255, 255), max_size=20, stroke=1)
    write_texture(rel_card, im_card)
    print('Patched', rel_card)

def patch_daily_roulette():
    rel = 'OutGame/DailyRoulette/Textures/tu_dr_train_select_base'
    im = load(rel)
    d = ImageDraw.Draw(im)
    # Route selection header
    d.rectangle([350, 62, 580, 115], fill=(70, 70, 75, 255))
    im, _ = draw_text(im, (355, 65, 575, 112), 'Route Selection', fontname='rodin_eb',
                      color=(255, 255, 255, 255), max_size=24, stroke=2)
    # Subtitle instructions
    d.rectangle([640, 62, 1650, 115], fill=(70, 70, 75, 255))
    im, _ = draw_text(im, (645, 65, 1645, 112), 'Please select a route (train model) for the roulette draw.',
                      fontname='rodin_m', color=(255, 255, 255, 255), max_size=20, stroke=1)
    write_texture(rel, im)
    print('Patched', rel)

def patch_options():
    # Brightness calibration
    rel_bc = 'OutGame/Option/Textures/tu_op_bc_base'
    im_bc = load(rel_bc)
    d_bc = ImageDraw.Draw(im_bc)
    d_bc.rectangle([20, 20, 105, 85], fill=(15, 15, 15, 255))
    im_bc, _ = draw_text(im_bc, (22, 22, 102, 82), 'Dark', fontname='rodin_eb',
                         color=(255, 255, 255, 255), max_size=24)
    d_bc.rectangle([1235, 20, 1315, 85], fill=(235, 235, 235, 255))
    im_bc, _ = draw_text(im_bc, (1238, 22, 1312, 82), 'Bright', fontname='rodin_eb',
                         color=(30, 30, 30, 255), max_size=24)
    write_texture(rel_bc, im_bc)
    print('Patched', rel_bc)

    # EMG on master controller
    rel_mc = 'OutGame/Option/Textures/tu_op_cc_mastercontrol_standard_base'
    im_mc = load(rel_mc)
    d_mc = ImageDraw.Draw(im_mc)
    d_mc.rectangle([98, 2, 162, 32], fill=(30, 30, 30, 255))
    im_mc, _ = draw_text(im_mc, (100, 2, 160, 30), 'EMG', fontname='bold',
                         color=(255, 255, 255, 255), max_size=18, stroke=1)
    write_texture(rel_mc, im_mc)
    print('Patched', rel_mc)

    # Near Zero badge
    rel_nz = 'OutGame/Option/Textures/tu_op_pd_nearzero_base'
    im_nz = load(rel_nz)
    d_nz = ImageDraw.Draw(im_nz)
    d_nz.rectangle([45, 25, 190, 105], fill=(30, 30, 30, 255))
    im_nz, _ = draw_text(im_nz, (48, 30, 186, 58), 'Close! 0cm', fontname='bold',
                         color=(255, 255, 255, 255), max_size=16, stroke=1)
    im_nz, _ = draw_text(im_nz, (48, 62, 186, 102), 'Near Zero', fontname='rodin_eb',
                         color=(255, 220, 50, 255), max_size=24, stroke=2)
    write_texture(rel_nz, im_nz)
    print('Patched', rel_nz)

    # Double Zero badge
    rel_wz = 'OutGame/Option/Textures/tu_op_pd_wzero_base'
    im_wz = load(rel_wz)
    d_wz = ImageDraw.Draw(im_wz)
    d_wz.rectangle([45, 10, 190, 115], fill=(30, 30, 30, 255))
    im_wz, _ = draw_text(im_wz, (48, 12, 186, 36), 'Stop 0cm', fontname='bold',
                         color=(255, 255, 255, 255), max_size=16, stroke=1)
    im_wz, _ = draw_text(im_wz, (48, 40, 186, 85), 'Double Zero', fontname='rodin_eb',
                         color=(255, 180, 50, 255), max_size=22, stroke=2)
    im_wz, _ = draw_text(im_wz, (48, 88, 186, 112), 'Perfect', fontname='bold',
                         color=(255, 255, 255, 255), max_size=14, stroke=1)
    write_texture(rel_wz, im_wz)
    print('Patched', rel_wz)

def main():
    patch_title_start()
    patch_main_menu_header()
    patch_save_progress()
    patch_mission_gauge()
    patch_mission_result()
    patch_total_result()
    patch_free_mode()
    patch_daily_roulette()
    patch_options()

    # Update jp_textures_verified.json
    verified_path = f'{W}/jp_textures_verified.json'
    v = json.load(open(verified_path, encoding='utf-8'))

    # List of textures patched by this script
    patched_keys = [
        'OutGame/Title/TitleTop_GameStartText_00',
        'OutGame/Title/TitleTop_GameStartText_01',
        'OutGame/MeinMenu/Textures/TU_MM_Header_02',
        'OutGame/SaveData/Textures/tu_save_progress_text_off',
        'OutGame/SaveData/Textures/tu_save_progress_text_on',
        'InGame/Common/Textures/TU_MG_GaugeBG',
        'InGame/MissionResult/Textures/TU_MR_TextArrivalTime01',
        'InGame/MissionResult/Textures/TU_MR_TextArrivalTime02',
        'InGame/MissionResult/Textures/TU_MR_TextDelay',
        'InGame/MissionResult/Textures/TU_MR_TextSecond',
        'InGame/TotalResult/Textures/TU_TotalResult_banner01',
        'InGame/TotalResult/Textures/TU_TotalResult_window01',
        'OutGame/FreeMode/Textures/TU_FM_k_1_02',
        'OutGame/FreeMode/Textures/TU_FM_k_2_01',
        'OutGame/FreeMode/Textures/TU_FM_k_2_02',
        'OutGame/FreeMode/Textures/TU_FM_k_2_03',
        'OutGame/FreeMode/Textures/TU_FM_k_3_01',
        'OutGame/FreeMode/Textures/TU_FM_k_3_02',
        'OutGame/FreeMode/Textures/TU_FM_right_bg_base',
        'OutGame/FreeMode/Textures/TU_FM_verification_card',
        'OutGame/DailyRoulette/Textures/tu_dr_train_select_base',
        'OutGame/Option/Textures/tu_op_bc_base',
        'OutGame/Option/Textures/tu_op_cc_mastercontrol_standard_base',
        'OutGame/Option/Textures/tu_op_pd_nearzero_base',
        'OutGame/Option/Textures/tu_op_pd_wzero_base',
    ]

    # Reclassify route strips to T9 (station name map cards)
    t9_route_names = [
        'InGame/BeforeDeparture/Textures/TU_BD_KTL_RouteName',
        'InGame/BeforeDeparture/Textures/TU_BD_NEX_RouteName',
        'InGame/BeforeDeparture/Textures/TU_BD_RouteName',
        'InGame/BeforeDeparture/Textures/TU_BD_RouteName_NT',
        'InGame/BeforeDeparture/Textures/TU_BD_SKL_RouteName',
        'InGame/BeforeDeparture/Textures/TU_BD_UTL_RouteName',
    ]

    # False positives (icons, backgrounds, english text, comic stickers)
    false_positives = [
        'InGame/MissionResult/Textures/TU_MR_Clear_Text',
        'OutGame/Scenario_NEW/Textures/TU_SC_difficulty_normal',
        'Common/Textures/TU_COM_PS4_BatsuBtn',
        'Common/Textures/TU_COM_PS4_CrossKey_LeftRight',
        'Common/Textures/tu_dr_mbg_YMTc205_snow_all',
        'InGame/BeforeDeparture/Textures/TU_BD_Flag_Goal',
        'InGame/BeforeDeparture/Textures/TU_BD_YMTRoute',
        'InGame/Common/Textures/TU_GG_Over_80',
        'InGame/Common/Textures/TU_MG_text_01',
        'InGame/Common/Textures/TU_MG_text_02',
        'InGame/Common/Textures/TU_PS_4_06',
        'OutGame/Common/Textures/TU_COM_Train_205',
        'OutGame/Common/Textures/TU_COM_Train_231',
        'OutGame/FreeMode/Textures/TU_BD_Flag_Start',
        'OutGame/FreeMode/Textures/TU_FM_1_02',
        'OutGame/FreeMode/Textures/TU_FM_1_03',
        'OutGame/FreeMode/Textures/TU_FM_1_05',
        'OutGame/FreeMode/Textures/TU_FM_1_08',
        'OutGame/FreeMode/Textures/TU_FM_route_station_curosr_active_goal',
        'OutGame/FreeMode/Textures/TU_FM_s_02',
        'OutGame/FreeMode/Textures/TU_FM_traintype_cursor_active',
        'OutGame/Option/Textures/tu_op_bc_screenshot',
        'OutGame/Option/Textures/tu_op_bg',
        'OutGame/SaveData/Textures/tu_save_background',
        'OutGame/Scenario_NEW/Textures/TU_SC_Info_RainRainbow_01',
        'OutGame/Scenario_NEW/Textures/TU_SC_Info_SunRainbow_01',
        'Common/Textures/TU_COM_Futaba_04',
        'Common/Textures/TU_COM_Futaba_09',
        'Common/Textures/TU_COM_Futaba_11',
        'Common/Textures/TU_COM_Futaba_13',
        'Common/Textures/TU_COM_Futaba_15',
    ]

    for k in patched_keys:
        if k in v:
            v[k]['patched'] = True

    for k in t9_route_names:
        if k in v:
            v[k]['task'] = 'T9'

    for k in false_positives:
        if k in v:
            v[k]['task'] = 'FalsePositive'
            v[k]['patched'] = True

    with open(verified_path, 'w', encoding='utf-8') as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

    print('Successfully updated jp_textures_verified.json! All T6 textures processed.')

if __name__ == '__main__':
    main()
