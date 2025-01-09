import os
import sys
import sdl2 as ss
import sdl2.ext as se
from sdl2.ext import Resources
from sdl2.ext.compat import byteify
import sdl2.sdlmixer as sm
import random

if getattr(sys, 'frozen', False):
    # running in a bundle
    filepy = sys.executable
else:
    # running live
    filepy = sys.argv[0]
fullpath = os.path.abspath(filepy)

#PTH_APP = 'D:/!BOOGMARKs/a/x9009'
PTH_APP = os.path.dirname(fullpath)

RESOURCES = Resources(PTH_APP, "resources")

pth_to_resources = PTH_APP + '/resources'
items = os.listdir(pth_to_resources)

RATE = 44100


if ss.SDL_Init(ss.SDL_INIT_AUDIO) != 0:
    raise RuntimeError("Cannot initialize audio system: {}".format(ss.SDL_GetError()))

if sm.Mix_OpenAudio(RATE, sm.MIX_DEFAULT_FORMAT, 2, 1):
    raise RuntimeError("Cannot open mixed audio: {}".format(sm.Mix_GetError()))
    
sm.Mix_AllocateChannels(9) # max is 9

factory = se.SpriteFactory(se.SOFTWARE)
sprite = factory.from_image(RESOURCES.get_path("background.png"))

def loadsample(filename=None):
    namefile = RESOURCES.get_path(filename)
    sample = sm.Mix_LoadWAV(byteify(namefile, "utf-8"))
    if sample is None:
        raise RuntimeError("Cannot open audio file: {}".format(sm.Mix_GetError()))
    sm.Mix_VolumeChunk(sample, 50)  # start VOL when LOAD
    return sample
    
smpls_organ_dict = {}

for item in items:
    if item[0] == 'o':
        splited = item.split('_', 1)
        name = splited[1].split('.')[0]
        namefile = RESOURCES.get_path(item)
        sample = sm.Mix_LoadWAV(byteify(namefile, "utf-8"))
        if sample is None:
            raise RuntimeError("Cannot open audio file: {}".format(sm.Mix_GetError()))
        sm.Mix_VolumeChunk(sample, 50) # start VOL when LOAD
        smpls_organ_dict[name] = sample

smpl_d_hihat = loadsample("d_hihat.wav")
smpl_d_hihat2 = loadsample("d_hihat.wav")
smpl_d_ohihat = loadsample("d_ohihat.wav")
smpl_d_ohihat2 = loadsample("d_ohihat.wav")
smpl_d_bass = loadsample("d_bass.wav")
smpl_d_bass2 = loadsample("d_bass.wav")
smpl_d_snare = loadsample("d_snare.wav")
smpl_d_ring = loadsample("d_ring.wav")
smpl_d_ring2 = loadsample("d_ring.wav")
smpl_d_plow = loadsample("d_plow.wav")
smpl_d_pclk = loadsample("d_pclk.wav")
smpl_d_phi = loadsample("d_phi.wav")

s_noise = loadsample("noise.wav")

s_bass_b01_e0 = loadsample("b01_e0.wav")
s_bass_b02_f0 = loadsample("b02_f0.wav")
s_bass_b03_f0sss = loadsample("b03_f0sss.wav")
s_bass_b04_g0 = loadsample("b04_g0.wav")
s_bass_b05_g0sss = loadsample("b05_g0sss.wav")
s_bass_b06_a0 = loadsample("b06_a0.wav")
s_bass_b07_a0sss = loadsample("b07_a0sss.wav")
s_bass_b08_b0 = loadsample("b08_b0.wav")
s_bass_b09_c1 = loadsample("b09_c1.wav")
s_bass_b10_c1sss = loadsample("b10_c1sss.wav")
s_bass_b11_d1 = loadsample("b11_d1.wav")
s_bass_b12_d1sss = loadsample("b12_d1sss.wav")

list_bass_samples_to_mute = [s_bass_b01_e0, s_bass_b02_f0, s_bass_b03_f0sss,
                              s_bass_b04_g0, s_bass_b05_g0sss, s_bass_b06_a0, s_bass_b07_a0sss,
                              s_bass_b08_b0, s_bass_b09_c1, s_bass_b11_d1, s_bass_b12_d1sss]

def play_bass_sample(e, press_status, numberkey, sample, list_bass_samples_to_mute, s_noise, VOL=0):
    if int(e.key.keysym.sym) == numberkey and not press_status:
        if e.type == ss.SDL_KEYDOWN:
            noise_cond_rand = random.randint(0, 100)
            sm.Mix_HaltChannel(5)
            if noise_cond_rand > 50:
                sm.Mix_HaltChannel(6)
            press_status = True
            channel = sm.Mix_PlayChannel(5, sample, 0)
            sm.Mix_VolumeChunk(sample, VOL+50)
            stereo_rand = random.randint(-30, 30)
            vol_dist_rand = random.randint(0,50)
            sm.Mix_SetPosition(5, stereo_rand, vol_dist_rand)
            if noise_cond_rand > 50:
                sm.Mix_PlayChannel(6, s_noise, 0)
            stereo_rand = random.randint(-80,80)
            sm.Mix_SetPosition(6, stereo_rand, 1000)

    if int(e.key.keysym.sym) == numberkey and press_status:
        if e.type == ss.SDL_KEYUP:
            press_status = False
    return press_status
    
channels_pressed = {'q': None, 'w': None, 'e': None, 'r': None, 't': None, 'y': None, 'u': None, 'i': None, 'o': None, 'p': None, '[': None, ']': None,
                   '1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, '9': None, '0': None, '-': None, '=': None}

channels_to_decey = []

 
def play_organ_sample(e, pressed, smpls_organ_dict, channels_pressed, numberkey=None, keybname='', notenamekey='', VOL=0):
    if int(e.key.keysym.sym) == numberkey and not pressed:
        if e.type == ss.SDL_KEYDOWN:
            sm.Mix_VolumeChunk(smpls_organ_dict[notenamekey], VOL)
            ch = sm.Mix_PlayChannel(-1, smpls_organ_dict[notenamekey], 20)
            stereo_rand = random.randint(-50, 50)
            vol_dist_rand = random.randint(80, 140)
            sm.Mix_SetPosition(ch, stereo_rand, vol_dist_rand)
            channels_pressed[keybname] = ch
            
            pressed = True
    if int(e.key.keysym.sym) == numberkey and pressed:
        if e.type == ss.SDL_KEYUP:
            sm.Mix_VolumeChunk(smpls_organ_dict[notenamekey], VOL)
            ch = channels_pressed[keybname]
            sm.Mix_HaltChannel(ch)
            channels_to_decey.append([notenamekey , smpls_organ_dict[notenamekey], VOL])
            pressed = False
    return pressed


def play_stop_sample(e, pressed, sample, numberkey=None, samplemute=None, samplemute2=None, volumeadd=0, channel_force=-1, VOL=0):
    if int(e.key.keysym.sym) == numberkey and not pressed:
        if e.type == ss.SDL_KEYDOWN:
            sm.Mix_VolumeChunk(sample, VOL+volumeadd)
            ch = sm.Mix_PlayChannel(channel_force, sample, 0)
            stereo_rand = random.randint(-10, 10)
            vol_dist_rand = random.randint(80,140)
            sm.Mix_SetPosition(ch, stereo_rand, vol_dist_rand)
            if samplemute != None:
                sm.Mix_VolumeChunk(samplemute, 0)
            if samplemute2 != None:
                sm.Mix_VolumeChunk(samplemute2, 0)
            pressed = True
    if int(e.key.keysym.sym) == numberkey and pressed:
        if e.type == ss.SDL_KEYUP:
            pressed = False
    return pressed


def run():
    se.init()
    window = se.Window("KHERO MouseWheel-Volume", size=(700, 330))
    window.show()
    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render(sprite)
    window.refresh()
    
    VOL = 50

    #  Drum Keys pressure or not pressure
    key_down_delete = False
    key_down_shift = False
    key_down_space = False
    key_down_left = False
    key_down_backspace = False
    key_down_down = False
    key_down_lctrl = False
    key_down_right = False
    key_down_up = False
    key_down_esc = False
    key_down_rctrl = False
    key_down_rshift = False
    key_down_return = False
    key_down_bslash = False
    bass_down_z = False
    bass_down_x = False
    bass_down_c = False
    bass_down_v = False
    bass_down_b = False
    bass_down_n = False
    bass_down_m = False
    bass_down_44 = False
    bass_down_46 = False
    bass_down_47 = False
    bass_down_a = False
    bass_down_s = False
    bass_down_d = False
    bass_down_f = False
    bass_down_g = False
    bass_down_h = False
    bass_down_j = False
    bass_down_k = False
    bass_down_l = False
    bass_down_59 = False
    bass_down_39 = False
    organ_down_q = False
    organ_down_w = False
    organ_down_e = False
    organ_down_r = False
    organ_down_t = False
    organ_down_y = False
    organ_down_u = False
    organ_down_i = False
    organ_down_o = False
    organ_down_p = False
    organ_down_brl = False
    organ_down_brr = False
    organ_down_1 = False
    organ_down_2 = False
    organ_down_3 = False
    organ_down_4 = False
    organ_down_5 = False
    organ_down_6 = False
    organ_down_7 = False
    organ_down_8 = False
    organ_down_9 = False
    organ_down_0 = False
    organ_down_minus = False
    organ_down_equal = False

    interval = 450000   # in ticks
    mcounter = interval
    metronome_is_play = False
    tick_counter = 0
    tap_counter = 0
    tick_prev4 = 0
    tick_prev3 = 0
    tick_prev2 = 0
    tick_prev1 = 0
    tap_reset_counter = 16
    scrollEnhance = 4
    running = True
    while running:
        events = se.get_events()
        tick_counter += 1
        if tick_counter > 9903962:
            tick_counter = 0
        mcounter -= 1
        
        if mcounter == 0:
            tap_reset_counter -= 1
            if  tap_reset_counter == 0:
                tap_reset_counter = 16
                tick_prev1,tick_prev2,tick_prev3,tick_prev4 = 0,0,0,0
                tap_counter = 0
            if metronome_is_play:
                sm.Mix_VolumeChunk(smpl_d_hihat, VOL-10)
                ch = sm.Mix_PlayChannel(-1, smpl_d_hihat, 0)
                mcounter = interval

        for event in events:
            if event.type == ss.SDL_QUIT:
                running = False
                break
            
            if int(event.key.keysym.sym) == 32: # MUTE BASS
                if event.type == ss.SDL_KEYDOWN: 
                    sm.Mix_HaltChannel(5)
                    sm.Mix_HaltChannel(6)
                    
            if event.type == ss.SDL_MOUSEWHEEL: # SET VOL
                # Mouse wheel event
                x = event.wheel.x
                if x < 0:
                    x -= scrollEnhance
                else:
                    x += scrollEnhance
                y = event.wheel.y
                if y < 0:
                    y -= scrollEnhance
                else:
                    y += scrollEnhance
                oldvol = VOL
                VOL += y
                if VOL > 70:
                    VOL = oldvol
                if VOL < 10:
                    VOL = oldvol
                
            if int(event.key.keysym.sym) == 1073742054: # TAP 
                if event.type == ss.SDL_KEYDOWN:
                    if tap_counter == 0:
                        tick_prev1 = tick_counter
                    elif tap_counter == 1:
                        tick_prev2 = tick_counter
                    elif tap_counter == 2:
                        tick_prev3 = tick_counter
                    else:
                        tick_prev4 = tick_counter
                    tap_counter += 1
                    sm.Mix_VolumeChunk(smpl_d_hihat, VOL-10)
                    ch = sm.Mix_PlayChannel(-1, smpl_d_hihat, 0)
                    if tap_counter > 3:
                        sm.Mix_VolumeChunk(smpl_d_hihat, VOL+10)
                        ch = sm.Mix_PlayChannel(-1, smpl_d_hihat, 0)
                        diff1 = tick_prev2-tick_prev1
                        diff2 = tick_prev3-tick_prev2
                        diff3 = tick_prev4-tick_prev3
                        ave_diff = (diff1+diff2+diff3)/3
                        interval = int(ave_diff)
                        mcounter = interval
                        tick_prev1,tick_prev2,tick_prev3,tick_prev4 = 0,0,0,0
                        tap_counter = 0
                        tick_counter = 0
                    
            if int(event.key.keysym.sym) == 1073742050:
                if event.type == ss.SDL_KEYDOWN:
                    if metronome_is_play:
                        metronome_is_play = False
                    else:
                        metronome_is_play = True
                        mcounter = 1

            # HIHATS DELTE AND L_SHIFT
            key_down_delete = play_stop_sample(event, key_down_delete, smpl_d_hihat, 127, smpl_d_ohihat, smpl_d_ohihat2, VOL)
            key_down_shift = play_stop_sample(event, key_down_shift, smpl_d_hihat2, 1073742049, smpl_d_ohihat, smpl_d_ohihat2, VOL)

            key_down_backspace = play_stop_sample(event, key_down_backspace, smpl_d_ohihat, 8, channel_force=8, VOL=VOL)
            key_down_down = play_stop_sample(event, key_down_down, smpl_d_ohihat2, 1073741905, channel_force=8, VOL=VOL)

            key_down_space = play_stop_sample(event, key_down_space, smpl_d_bass, 9, volumeadd=40, VOL=VOL) # TAB
            key_down_left = play_stop_sample(event, key_down_left, smpl_d_bass2, 1073741904, volumeadd=40, VOL=VOL)

            key_down_lctrl = play_stop_sample(event, key_down_lctrl, smpl_d_snare, 1073742048, VOL=VOL)
            key_down_right = play_stop_sample(event, key_down_right, smpl_d_snare, 1073741903, VOL=VOL)
            key_down_up = play_stop_sample(event, key_down_up, smpl_d_snare, 1073741906, VOL=VOL)

            key_down_esc = play_stop_sample(event, key_down_esc, smpl_d_ring, 27, volumeadd=5, channel_force=7, VOL=VOL)
            key_down_rctrl = play_stop_sample(event, key_down_rctrl, smpl_d_ring2, 1073742052, volumeadd=5, channel_force=7, VOL=VOL)

            key_down_rshift = play_stop_sample(event, key_down_rshift, smpl_d_plow, 1073742053, VOL=VOL)
            key_down_return = play_stop_sample(event, key_down_return, smpl_d_pclk, 13, VOL=VOL)
            key_down_bslash = play_stop_sample(event, key_down_bslash, smpl_d_phi, 92, VOL=VOL)

            bass_down_z = play_bass_sample(event, bass_down_z, 122, s_bass_b09_c1, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_x = play_bass_sample(event, bass_down_x, 120, s_bass_b05_g0sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_c = play_bass_sample(event, bass_down_c, 99, s_bass_b02_f0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_v = play_bass_sample(event, bass_down_v, 118, s_bass_b10_c1sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_b = play_bass_sample(event, bass_down_b, 98, s_bass_b07_a0sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_n = play_bass_sample(event, bass_down_n, 110, s_bass_b03_f0sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_m = play_bass_sample(event, bass_down_m, 109, s_bass_b12_d1sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_44 = play_bass_sample(event, bass_down_44, 44, s_bass_b08_b0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_46 = play_bass_sample(event, bass_down_46, 46, s_bass_b05_g0sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_47 = play_bass_sample(event, bass_down_47, 47, s_bass_b11_d1, list_bass_samples_to_mute, s_noise, VOL=VOL)

            bass_down_a = play_bass_sample(event, bass_down_a, 97, s_bass_b01_e0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_s = play_bass_sample(event, bass_down_s, 115, s_bass_b10_c1sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_d = play_bass_sample(event, bass_down_d, 100, s_bass_b06_a0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_f = play_bass_sample(event, bass_down_f, 102, s_bass_b03_f0sss, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_g = play_bass_sample(event, bass_down_g, 103, s_bass_b11_d1, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_h = play_bass_sample(event, bass_down_h, 104, s_bass_b08_b0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_j = play_bass_sample(event, bass_down_j, 106, s_bass_b04_g0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_k = play_bass_sample(event, bass_down_k, 107, s_bass_b01_e0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_l = play_bass_sample(event, bass_down_l, 108, s_bass_b09_c1, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_59 = play_bass_sample(event, bass_down_59, 59, s_bass_b06_a0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            bass_down_39 = play_bass_sample(event, bass_down_39, 39, s_bass_b02_f0, list_bass_samples_to_mute, s_noise, VOL=VOL)
            
            organ_down_q = play_organ_sample(event, organ_down_q, smpls_organ_dict, channels_pressed, 113, 'q', 'G1', VOL=VOL)
            organ_down_w = play_organ_sample(event, organ_down_w, smpls_organ_dict, channels_pressed, 119, 'w', 'D1_sharp', VOL=VOL)
            organ_down_e = play_organ_sample(event, organ_down_e, smpls_organ_dict, channels_pressed, 101, 'e', 'C2', VOL=VOL)
            organ_down_r = play_organ_sample(event, organ_down_r, smpls_organ_dict, channels_pressed, 114, 'r', 'G1_sharp', VOL=VOL)
            organ_down_t = play_organ_sample(event, organ_down_t, smpls_organ_dict, channels_pressed, 116, 't', 'F1', VOL=VOL)
            organ_down_y = play_organ_sample(event, organ_down_y, smpls_organ_dict, channels_pressed, 121, 'y', 'C2_sharp', VOL=VOL)
            organ_down_u = play_organ_sample(event, organ_down_u, smpls_organ_dict, channels_pressed, 117, 'u', 'A1_sharp', VOL=VOL)
            organ_down_i = play_organ_sample(event, organ_down_i, smpls_organ_dict, channels_pressed, 105, 'i', 'F1_sharp', VOL=VOL)
            organ_down_o = play_organ_sample(event, organ_down_o, smpls_organ_dict, channels_pressed, 111, 'o', 'D1_sharp', VOL=VOL)
            organ_down_p = play_organ_sample(event, organ_down_p, smpls_organ_dict, channels_pressed, 112, 'p', 'B1', VOL=VOL)
            organ_down_brl = play_organ_sample(event, organ_down_brl, smpls_organ_dict, channels_pressed, 91, '[', 'G1_sharp', VOL=VOL)
            organ_down_brr = play_organ_sample(event, organ_down_brr, smpls_organ_dict, channels_pressed, 93, ']', 'E1', VOL=VOL)
            
            organ_down_1 = play_organ_sample(event, organ_down_1, smpls_organ_dict, channels_pressed, 49, '1', 'E1', VOL=VOL)
            organ_down_2 = play_organ_sample(event, organ_down_2, smpls_organ_dict, channels_pressed, 50, '2', 'C2_sharp', VOL=VOL)
            organ_down_3 = play_organ_sample(event, organ_down_3, smpls_organ_dict, channels_pressed, 51, '3', 'A1', VOL=VOL)
            organ_down_4 = play_organ_sample(event, organ_down_4, smpls_organ_dict, channels_pressed, 52, '4', 'F1_sharp', VOL=VOL)
            organ_down_5 = play_organ_sample(event, organ_down_5, smpls_organ_dict, channels_pressed, 53, '5', 'D2', VOL=VOL)
            organ_down_6 = play_organ_sample(event, organ_down_6, smpls_organ_dict, channels_pressed, 54, '6', 'B1', VOL=VOL)
            organ_down_7 = play_organ_sample(event, organ_down_7, smpls_organ_dict, channels_pressed, 55, '7', 'G1', VOL=VOL)
            organ_down_8 = play_organ_sample(event, organ_down_8, smpls_organ_dict, channels_pressed, 56, '8', 'E1', VOL=VOL)
            organ_down_9 = play_organ_sample(event, organ_down_9, smpls_organ_dict, channels_pressed, 57, '9', 'C2', VOL=VOL)
            organ_down_0 = play_organ_sample(event, organ_down_0, smpls_organ_dict, channels_pressed, 48, '0', 'A1', VOL=VOL)
            organ_down_minus = play_organ_sample(event, organ_down_minus, smpls_organ_dict, channels_pressed, 45, '-', 'F1', VOL=VOL)
            organ_down_equal = play_organ_sample(event, organ_down_equal, smpls_organ_dict, channels_pressed, 61, '=', 'D2', VOL=VOL)

        for ch_dec in channels_to_decey:
            ch_dec[2] -= 0.002
            if event.type == ss.SDL_KEYUP:
                sm.Mix_VolumeChunk(smpls_organ_dict[ch_dec[0]], 10)
                ch = sm.Mix_PlayChannel(6, smpls_organ_dict[ch_dec[0]], 0)
                stereo_rand = random.randint(-50, 50)
                vol_dist_rand = random.randint(80, 140)
                sm.Mix_SetPosition(ch, stereo_rand, vol_dist_rand)
            if ch_dec[2] < 5:
                channels_to_decey.remove(ch_dec)

    return 0

run()
sm.Mix_CloseAudio()
ss.SDL_Quit(ss.SDL_INIT_AUDIO)
se.quit()
