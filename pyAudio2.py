import pyaudio
import speech_recognition as sr

# 聲音設置
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
rate = 44100
record_seconds = 3

# 創建PyAudio對象
p = pyaudio.PyAudio()

# 開始錄音
def record_audio():
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    return b''.join(frames)

# 語音指令辨識
def recognize_speech(audio):
    recognizer = sr.Recognizer()
    try:
        # 調用Google語音識別API
        text = recognizer.recognize_google(audio, language="zh-TW")
        print("辨識結果: " + text)
        if "開門" in text:
            print("正在開門...")
            # 開門程式碼
        elif "關門" in text:
            print("正在關門...")
            # 關門程式碼
        else:
            print("指令未識別")
    except sr.UnknownValueError:
        print("識別失敗")

while True:
    print("等待指令...")
    audio = record_audio()
    recognize_speech(audio)
