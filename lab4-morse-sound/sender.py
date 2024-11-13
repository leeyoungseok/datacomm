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

CHANNELS = 1
SAMPLERATE = 48000
FREQUENCY = 261.626
#FREQUENCY = 523.251
UNIT = 0.1

SHORTMAX = 2**(32-1)-1
MORSE_THRESHOLD = SHORTMAX // 4
UNSEEN_THRESHOLD = 3.0

def text2morse(text):
    text = text.upper()
    morse = ''

    for t in text:
        if t == ' ':
            morse = morse + '/' # / after a word
        for key, value in morsecode.code.items():
            if t == key:
                morse = morse + value
        morse = morse + ' '  # space after each alphabet 

    return morse[:-1]

def morse2audio(morse):
    audio = []
    for m in morse:
        if m == '.':
            for i in range(math.ceil(SAMPLERATE*UNIT)*1):
                audio.append(int(SHORTMAX*math.sin(2*math.pi*FREQUENCY*i/SAMPLERATE)))
        elif m == '-':
            for i in range(math.ceil(SAMPLERATE*UNIT)*3):
                audio.append(int(SHORTMAX*math.sin(2*math.pi*FREQUENCY*i/SAMPLERATE)))
        elif m == ' ': # after each alpahbet
            for i in range(math.ceil(SAMPLERATE*UNIT)*1):
                audio.append(int(0))
        elif m == '/': # after each word
            for i in range(math.ceil(SAMPLERATE*UNIT)*1):
                audio.append(int(0))
        for i in range(math.ceil(SAMPLERATE*UNIT)*1):
            audio.append(int(0))
    return audio

def audio2file(audio, filename):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(48000)
        for a in audio:
            w.writeframes(struct.pack('<l', a))

def send_data():
    text = input('User input: ').strip()

    morse = text2morse(text)
    print(f'MorseCode: {morse}')
    audio = morse2audio(morse)
    audio2file(audio, "test.wav")
    print(f'You have written wave audio to test.wav file !!!')

if __name__ == '__main__':
    send_data() # text2morse() -> morse2audio() -> audio2file() 