import os
import wave
import struct

import reedsolo
import scipy.fftpack
import numpy as np

FLAGS = _ = None
DEBUG = False
SHORTMAX = 2**(16-1)-1
HEX_LIST = ['0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E',
            'F']
HEX_SET = set(HEX_LIST)


def create_rules(freq_start, freq_step):
    rules = {}
    rules['START'] = freq_start
    for i in range(len(HEX_LIST)):
        h = HEX_LIST[i]
        rules[h] = freq_start + freq_step + freq_step*(i+1)
    rules['END'] = freq_start + freq_step + freq_step*(len(HEX_LIST)) + freq_step*2
    return rules

def audio2freq(audio, samplerate):
    freq = scipy.fftpack.fftfreq(len(audio))
    fourier = scipy.fftpack.fft(audio)
    top = freq[np.argmax(abs(fourier))]*samplerate
    #print("in audio2freq: top ", top)
    return top

def freq2hex(fft_top, rules, padding):
    for k, v in rules.items():
        if v-padding <= fft_top and fft_top <= v+padding:
            #print("k, v", k, v, padding)
            return k
    return None
            
def file2hex(filename, rules, unit, samplerate, padding):
    string_hex = ''
    with wave.open(filename, 'rb') as w:
        framerate = w.getframerate()
        frames = w.getnframes()
        status_code = 'START'
        status_count = 0
        audio_data = []
        audio_count = 0
        for i in range(frames):
            frame = w.readframes(1)
            d = struct.unpack('<h', frame)[0]
            audio_data.append(d)
            audio_count = audio_count + 1
            if status_code == 'START':
                if audio_count >= (unit*samplerate/10):
                    fft_top = audio2freq(audio_data, samplerate)
                    word = freq2hex(fft_top, rules, padding)
                    if word == 'START':
                        status_count = status_count + 1
                        audio_data.clear()
                        audio_count = 0
                    elif status_count >= 2*10-1:
                        status_code = 'DATA'
                    else:
                        status_count = 0
                        audio_data.clear()
                        audio_count = 0
                    if DEBUG:
                        print(fft_top, word, status_code, status_count)
            elif status_code == 'DATA':
                if audio_count >= unit*samplerate:
                    fft_top = audio2freq(audio_data, samplerate)
                    word = freq2hex(fft_top, rules, padding)
                    if word == 'END':
                        status_count = status_count + 1
                    else:
                        string_hex = f'{string_hex}{word}'
                        status_count = 0
                    audio_data.clear()
                    audio_count = 0
                    if DEBUG:
                        print(fft_top, word, status_code, status_count)
                    if status_count >= 2:
                        status_code = 'END'
                        break
    return string_hex


def hex2text(result_hex, data_len, rsc_len):
    byte_hex = bytes.fromhex(result_hex)

    rsc = reedsolo.RSCodec(FLAGS.rsc_len)
    string_hex = ''
    for k in range(0, len(byte_hex), FLAGS.data_len+FLAGS.rsc_len):
        data = byte_hex[k:k+FLAGS.data_len+FLAGS.rsc_len]
        decoded_data = rsc.decode(data)[0].hex().upper()
        string_hex = f'{string_hex}{decoded_data}'
        if DEBUG:
            print("decoded_data: ", f'{decoded_data}')
    
    result_string = bytes.fromhex(string_hex).decode('utf-8')
    return result_string


def main():
    rules = create_rules(FLAGS.freq_start, FLAGS.freq_step)
    if DEBUG:
        print('The data over sound rules:')
        for k, v in rules.items():
            print(f'{k} {v}')
        print('-----')
            
    result_hex = file2hex(FLAGS.input, rules, FLAGS.unit, FLAGS.samplerate, FLAGS.padding)
    print("result_hex: ", result_hex)
    result_string = hex2text(result_hex, FLAGS.data_len, FLAGS.rsc_len)
    print("hex2text: ", result_string)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--input', type=str, required=True,
                        help='Input wav file')
    parser.add_argument('--unit', type=float, default=0.1,
                        help='The unit size (seconds)')
    parser.add_argument('--samplerate', type=int, default=48000,
                        help='The sample rate')
    parser.add_argument('--padding', type=int, default=32,
                        help='The padding for noise')
    parser.add_argument('--rsc_len', type=int, default=4,
                        help='The Reed solomon code size')
    parser.add_argument('--data_len', type=int, default=12,
                        help='The data size')
    parser.add_argument('--freq_start', type=float, default=512,
                        help='The start frequency')
    parser.add_argument('--freq_step', type=float, default=128,
                        help='The step frequency')
    
    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    
    
    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))

    main()
