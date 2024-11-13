import wave
import struct
import scipy.fftpack
import numpy as np
import os
from frequence_rule import get_freq_rule

unit = 0.1
samplerate = 48000
padding = 5
rules = get_freq_rule()


class Receiver():
    def __init__(self, filename:str) -> None:
        self.filename = filename
        self.text =''

    def read_wav_file(self):
        """
        WAV 파일을 읽어와서 오디오 신호와 샘플링 레이트를 반환하는 함수

        입력 :  filename (str): WAV 파일의 경로
        반환 :  audio 오디오 신호, framerate 샘플링 레이트
        """
        with wave.open(self.filename, 'rb') as w:
            framerate = w.getframerate()
            frames = w.getnframes()
            audio = []
            for i in range(frames):
                frame = w.readframes(1)
                d = struct.unpack('<h', frame)[0]
                audio.append(d)
            return audio, framerate

    def get_top_freq(self, audio, samplerate):
        """
        주어진 오디오 신호에서 주파수 스펙트럼을 계산하여 
        가장 큰 진폭을 가진 주파수를 반환하는 함수

        입력:
            audio (list): 오디오 신호 데이터가 담긴 리스트
            samplerate (int): 샘플링 레이트

        반환:
            top(float): 주파수 스펙트럼에서 가장 큰 진폭을 가진 주파수
        """
        freq = scipy.fftpack.fftfreq(len(audio))
        fourier = scipy.fftpack.fft(audio)
        top = freq[np.argmax(abs(fourier))]*samplerate
        return top

    def decode_sound(self, audio, samplerate, rules:dict, unit, padding):
        """
        주어진 오디오 신호에서 음성 인식을 수행하여 디코딩된 문자열을 반환하는 함수

        입력:
            audio (list): 오디오 신호 데이터가 담긴 리스트
            samplerate (int): 샘플링 레이트
            rules (dict): 주파수 규칙을 담은 딕셔너리
            unit (float): 오디오 신호를 쪼갤 단위 시간
            padding (int): 인식된 주파수와 일치하는 규칙 주파수의 허용 오차 범위

        반환:
            text(str): 디코딩된 문자열
        """
        text = ''
        for i in range(0, len(audio), int(unit * samplerate)):
            curr_audio = audio[i: i + int(unit * samplerate)]
            top_freq = self.get_top_freq(curr_audio, samplerate)
            data = ''
            for k, v in rules.items():
                if v - padding <= top_freq and top_freq <= v + padding:
                    data = k
            if data != 'START' and data != 'END':
                text += data
        
        self.text = bytes.fromhex(text).decode("utf-8")
        return self.text
    

if __name__ == '__main__':
    dir_list = os.listdir('./')
    wav_name = ''
    filename = ''
    for file in dir_list:
        if '.wav' in file:
            _ = file.split('.')
            try:
                student_number = int(_[0])
                filename = file
                if type(student_number) == int:
                    wav_name = _[0]
            except:
                print("student number wav file doesn't exists")
    
    receiver = Receiver(filename=filename)
    audio, framerate = receiver.read_wav_file()
    text = receiver.decode_sound(audio, samplerate, rules, unit, padding)
    print(f'Decoded: {text}')