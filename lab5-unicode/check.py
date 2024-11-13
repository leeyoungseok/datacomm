from frequence_rule import get_freq_rule
from extract_text import get_target
from send_unicode import Sender
from receive_unicode import Receiver
import os
import random

SHORTMAX = 2**(16-1)-1
CHANNELS = 1
UNIT = 0.1
SAMPLERATE = 48000
PADDING = 5

def test_one():
    sender = Sender(text='🧡💛💚💙', filename='test_one.wav')
    sender.make_audio(unit=UNIT, samplerate=SAMPLERATE, rules=get_freq_rule(), string_hex=sender.string_hex)
    assert sender.freq == [2688, 768, 1920, 2688, 2048, 1664, 2048, 896, 2688, 768, 1920, 2688, 1920, 1024, 1920, 2176, 2688, 768, 1920, 2688, 1920, 1024, 1920, 2048, 2688, 768, 1920, 2688, 1920, 1024, 1920, 1920]
    
def test_two():
    sender = Sender(text='👀🦴', filename='test_two.wav')
    sender.make_audio(unit=UNIT, samplerate=SAMPLERATE, rules=get_freq_rule(), string_hex=sender.string_hex)
    assert sender.freq == [2688, 768, 1920, 2688, 1920, 896, 1792, 768, 2688, 768, 1920, 2688, 2048, 1536, 2176, 1280]
    
def test_three():
    sender = Sender(text='🐵🐆🦜', filename='test_three.wav')
    sender.make_audio(unit=UNIT, samplerate=SAMPLERATE, rules=get_freq_rule(), string_hex=sender.string_hex)
    assert sender.freq == [2688, 768, 1920, 2688, 1920, 768, 2176, 1408, 2688, 768, 1920, 2688, 1920, 768, 1792, 1536, 2688, 768, 1920, 2688, 2048, 1536, 1920, 2304]
    
def test_four():
    dir_list = os.listdir('./')
    wav_name = ''
    file_name = ''
    for file in dir_list:
        if '.wav' in file:
            _ = file.split('.')
            try:
                student_number = int(_[0])
                if type(student_number) == int:
                    wav_name = student_number
                    file_name = file
            except:
                print("student number wav file doesn't exists")
                exit()
    
    receiver = Receiver(filename=file_name)
    audio, framerate = receiver.read_wav_file()
    text = receiver.decode_sound(audio,samplerate = SAMPLERATE, rules=get_freq_rule(), unit = UNIT, padding = PADDING)
    
    answer = get_target(wav_name)
    print(answer, text)
    
    assert receiver.text == answer
    
def test_five():
    
    file_number = random.randint(200000000, 203000000)
    file_name = str(file_number)+'.wav'
    
    sender = Sender(text = get_target(file_number), filename=file_name)
    audio = sender.make_audio(unit=UNIT, samplerate=SAMPLERATE, rules=get_freq_rule(), string_hex=sender.string_hex)
    sender.audio2file(audio=audio, 
            filename= sender.filename, 
            channel=CHANNELS, 
            sampwidth=2, 
            samplerate=SAMPLERATE)
    
    receiver = Receiver(filename=file_name)
    audio, framerate = receiver.read_wav_file()
    text = receiver.decode_sound(audio=audio, samplerate = SAMPLERATE, rules=get_freq_rule(), unit = UNIT, padding = PADDING)
    
    assert sender.text == receiver.text
