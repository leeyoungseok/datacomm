import math
import struct
# import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt 
import scipy.fftpack as fftpack
from frequence_rule import get_freq_rule
from extract_text import get_target

## 글로벌 변수 수정하지 말기
SHORTMAX = 2**(16-1)-1
CHANNELS = 1
UNIT = 0.1
SAMPLERATE = 48000

class Sender():
    def __init__(self, text:str, filename:str) -> None:
        self.text = text
        self.filename = filename
        self.string_hex = text.encode('utf-8').hex().upper()
        self.freq = []
        
    def make_audio(self, unit, samplerate, rules, string_hex):
        '''
        사인파 만들기
        audio 배열에 사인파 공식으로 음원정보 담기 
        '''
        audio = []
        
        print(f"START STRING : -> FREQ : {rules['START']}")
        print(f"START STRING : -> FREQ : {rules['START']}")
        for i in range(int(unit*samplerate*2)): # 2배, 전송 시작 싱크 맞추기 위해 2번 음원 생성
            audio.append(SHORTMAX*math.sin(2*math.pi*rules['START']*i/samplerate))
            
        for s in string_hex:
            print(f"STRING : {s} -> FREQ : {rules[s]}")
            self.freq.append(rules[s])
            for i in range(int(unit*samplerate*1)):
                audio.append(SHORTMAX*math.sin(2*math.pi*rules[s]*i/samplerate))
                
        print(f"END STRING : -> FREQ : {rules['END']}")
        print(f"END STRING : -> FREQ : {rules['END']}")
        for i in range(int(unit*samplerate*2)): # 2배, 전송 종료 싱크 맞추기 위해 2번 음원 생성
            audio.append(SHORTMAX*math.sin(2*math.pi*rules['END']*i/samplerate))        
        return audio

    # def play2audio(self, audio, channels, samplerate):
    #     '''
    #     pyaudio로 만든 audio 재생
    #     '''
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=pyaudio.paInt16,
    #                     channels=channels,
    #                     rate=samplerate,
    #                     frames_per_buffer=samplerate,
    #                     output=True)
    #     for a in audio:
    #         stream.write(struct.pack('<h', int(a)))


    def audio2file(self, audio, filename, channel, sampwidth, samplerate):
        '''
        사인파 음원파일 audio를 파일로 저장
        '''
        with wave.open(filename, 'wb') as w:
            w.setnchannels(channel)
            w.setsampwidth(sampwidth)
            w.setframerate(samplerate)
            for a in audio:
                w.writeframes(struct.pack('<h', int(a)))

    def plot_audio(self, audio):
        '''
        1. 사인파 그래프 그리기
        2. 푸리에변환으로 주파수 영역 시각화
        '''
        t = np.arange(len(audio)) / float(SAMPLERATE)
        
        # FFT 적용
        fft_data = abs(fftpack.fft(audio)) / len(audio)
        # 주파수 범위 생성
        freq = fftpack.fftfreq(len(audio)) * SAMPLERATE
        
        # 음성 데이터 그래프로 시각화
        fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(20, 6))
        ax[0].plot(t, audio)
        ax[0].set_ylabel('Amplitude')
        ax[1].plot(t, audio)
        ax[1].set_xlim(0.0, 0.2)
        ax[1].set_ylabel('Amplitude')
        ax[1].set_xlabel('Time (s)')
        
        ax[2].plot(t, audio)
        ax[2].set_xlim(0.2, 0.4)
        ax[2].set_ylabel('Amplitude')
        ax[2].set_xlabel('Time (s)')
        
        # 음성 데이터 to 주파수
        ax[3].plot(freq, fft_data)
        ax[3].set_xlim(0, 1000)
        ax[3].set_ylabel('Magnitude')
        ax[3].set_xlabel('Frequency (Hz)')
        xticks = np.arange(500, 1000, 100)
        ax[3].set_xticks(xticks)
        
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=None, hspace=0.5)
        plt.show()

if __name__ == '__main__':
    # OS별 이모지 입력 방법
    # 1. 윈도우즈 : 윈도우즈 10 이상의 경우, Win + .(마침표) 키.
    # 2. 맥 :  Ctrl + Cmd + Spacebar  
    # 3. 우분투 :  GNOME 데스크톱 환경에서는 Ctrl + Shift + e를 누르고 이모지 코드 포인트를 입력해야함
    # - 코드 포인트를 다 입력할 수가 없으므로 본 코드에서 제공되는 샘플 이모지를 활용하는걸 추천 
    # - 샘플 '🧡💛💚💙💜🐶🐵🐆🦜👀🦴'
    
    print("TYPE YOUR STUDENT NUMBER: ")
    student_number = int(input())
    text = get_target(student_number)
    
    sender = Sender(text=text, filename=f'{student_number}.wav')
    #sender.stringhex = sender.text.encode('utf-8').hex().upper()
    
    print(f'INPUT TEXT : {sender.text}')
    print(f'INPUT TEXT to STRING HEX : {sender.string_hex}')
    print(f'-'*20)
    
    rules = get_freq_rule()
    audio = sender.make_audio(unit=UNIT,
                       samplerate=SAMPLERATE,
                       rules=rules,
                       string_hex=sender.string_hex)
    
    sender.audio2file(audio=audio, 
               filename= sender.filename, 
               channel=CHANNELS, 
               sampwidth=2, 
               samplerate=SAMPLERATE)
    # 아래 코드들은 자동채점할 시 반드시 주석처리 해야함.
    sender.plot_audio(audio=audio)
    #sender.play2audio(audio=audio, channels=CHANNELS, samplerate=SAMPLERATE)
