import os
import sys
import re
import math
import wave
import struct
import statistics
import time
import pyaudio
import morsecode

FLAGS = _ = None
DEBUG = False
CHANNELS = 1

SAMPLERATE = 48000
FREQUENCY = 261.626
#FREQUENCY = 523.251
UNIT = 0.1

SHORTMAX = 2**(32-1)-1
MORSE_THRESHOLD = SHORTMAX // 4
UNSEEN_THRESHOLD = 3.0

def file2morse2(filename):
    with wave.open(filename, 'rb') as w:
        audio = []
        framerate = w.getframerate()
        frames = w.getnframes()
        print("frame count: ", frames)
        for i in range(frames):
            frame = w.readframes(1)
            audio.append(struct.unpack('<i', frame)[0])  # 16비트 오디오를 위해 '<h' 사용
        morse = ''
        unit = int(0.1 * framerate)  # 프레임 속도를 기반으로 단위 계산
        threshold = 10000
        print("len(audio)", len(audio))
        for i in range(0, len(audio), unit):
            chunk = audio[i:i+unit]
            avg_amplitude = sum(abs(x) for x in chunk) / len(chunk)
            
            if avg_amplitude > threshold:  # 점/대시를 위한 임계값을 정의하세요
                morse += '.'
            else:
                morse += ' '
        morse = morse.replace('...', '-')
        morse = morse.strip().replace('       ','m').replace('   ', 's').replace(' ', '').replace('s', ' ').replace('m', ' / ')
    
    return morse

def file2morse(filename):
    with wave.open(filename, 'rb') as w:
        audio = []
        framerate = w.getframerate()
        frames = w.getnframes()
        print("frame count: ", frames)
        for i in range(frames):
            frame = w.readframes(1)
            audio.append(struct.unpack('<i', frame)[0])
        morse = ''
        unit = int(0.1 * 48000)
        print("unit: ", unit)
        print("len(audio): ", len(audio))
        print("len(audio)/unit): ", len(audio)/unit)
        for i in range(1, math.ceil(len(audio)/unit)+1):
            stdev = statistics.stdev(audio[(i-1)*unit:i*unit])
            if stdev > 10000:
                morse = morse + '.'
            else:
                morse = morse + ' '
        morse = morse.replace('...', '-')
    
    morse = morse.strip()
    morse = morse.replace('...', '-')
    morse = morse.replace('       ', 'm') # space after word
    morse = morse.replace('   ', 's') # space after alphabet
    morse = morse.replace(' ', '')
    morse = morse.replace('s', ' ')
    morse = morse.replace('m', ' / ')
    morse = morse

    return morse

def morse2text(morse):
    text = ''
    for code in morse.split(' '):
        if code == '/':
            text = text + ' '
        for key, value in morsecode.code.items():
            if code == value:
                text = text + key
    return text

def read_data():
    morse = file2morse2("test.wav")
    print(f'Morse: {morse}')
    text = morse2text(morse)
    print(f'Sound input: {text}')

def main():
    print('Receive data from file')
    read_data()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='The present debug message')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

