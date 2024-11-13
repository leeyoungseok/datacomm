import os
import csv
import math
import random
import wave
import struct

import reedsolo

FLAGS = _ = None
DEBUG = False
SHORTMAX = 2**(16-1)-1
HEX_LIST = ['0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E',
            'F']
HEX_SET = set(HEX_LIST)
# RULES = {'START': 512,
#          '0': 768,
#          '1': 896,
#          '2': 1024,
#          '3': 1152,
#          '4': 1280,
#          '5': 1408,
#          '6': 1536,
#          '7': 1664,
#          '8': 1792,
#          '9': 1920,
#          'A': 2048,
#          'B': 2176,
#          'C': 2304,
#          'D': 2432,
#          'E': 2560,
#          'F': 2688,
#          'END': 2944}


def read_csv(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['Number'], row['P1']

def create_rules(freq_start, freq_step):
    rules = {}
    rules['START'] = freq_start
    for i in range(len(HEX_LIST)):
        h = HEX_LIST[i]
        rules[h] = freq_start + freq_step + freq_step*(i+1)
    rules['END'] = freq_start + freq_step + freq_step*(len(HEX_LIST)) + freq_step*2
    return rules

def create_p1(string, rules, unit, samplerate, data_len, rsc_len): # Clean audio
    audio = []
    
    data_hex = string.encode('utf-8')
    data_string = data_hex.hex().upper()

    for i in range(int(unit*samplerate*2)):
        audio.append(SHORTMAX*math.sin(2*math.pi*rules['START']*i/samplerate))
    
    client_rsc = reedsolo.RSCodec(rsc_len)
    for k in range(0, len(data_hex), data_len):
        data = data_hex[k:k+data_len]
        encoded_data = client_rsc.encode(data).hex().upper()
        for s in encoded_data:
            for i in range(int(unit*samplerate)):
                audio.append(SHORTMAX*math.sin(2*math.pi*rules[s]*i/samplerate))
        
    for i in range(int(unit*samplerate*2)):
        audio.append(SHORTMAX*math.sin(2*math.pi*rules['END']*i/samplerate))
    
    return audio

def audio2file(audio, filename, channel, sampwidth, samplerate):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(channel)
        w.setsampwidth(sampwidth)
        w.setframerate(samplerate)
        for a in audio:
            w.writeframes(struct.pack('<h', int(a)))
            
def main():
    rules = create_rules(FLAGS.freq_start, FLAGS.freq_step)
    if DEBUG:
        print('The data over sound rules:')
        for k, v in rules.items():
            print(f'{k} {v}')
        print('-----')

    os.makedirs(FLAGS.output, exist_ok=True)
    for number, p1 in read_csv(FLAGS.input):
        if DEBUG:
            print(f'{number}, {p1}')
        audio = create_p1(p1, rules, FLAGS.unit, FLAGS.samplerate, FLAGS.data_len, FLAGS.rsc_len)
        filename = os.path.join(FLAGS.output, f'{number}-p1.wav')
        audio2file(audio, filename, FLAGS.channel, FLAGS.sampwidth, FLAGS.samplerate)
        if DEBUG:
            print(f'{number} {filename} created for {p1}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--input', type=str, required=True,
                        help='Input csv file (Fieldnames: Number, P1, P2, P3)')
    parser.add_argument('--unit', type=float, default=0.1,
                        help='The unit size (seconds)')
    parser.add_argument('--samplerate', type=int, default=48000,
                        help='The sample rate')
    parser.add_argument('--channel', type=int, default=1,
                        help='The channel')
    parser.add_argument('--sampwidth', type=int, default=2,
                        help='The Sample width')
    parser.add_argument('--rsc_len', type=int, default=4,
                        help='The Reed solomon code size')
    parser.add_argument('--data_len', type=int, default=12,
                        help='The data size')
    parser.add_argument('--freq_start', type=float, default=512,
                        help='The start frequency')
    parser.add_argument('--freq_step', type=float, default=128,
                        help='The step frequency')
    parser.add_argument('--output', type=str, default='problems',
                        help='The output directory')
    
    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    
    
    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    main()