import pyaudio
import wave
import speech_recognition as sr



# 配置錄音參數
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"

# 創建PyAudio對象
audio = pyaudio.PyAudio()

# 開始錄音
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("Recording for 5 seconds...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

# 結束錄音
stream.stop_stream()
stream.close()
audio.terminate()
print("Finish record and Stop Stream...")

# 保存錄音文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
print("Saving the record....")


# 創建Recognizer對象
r = sr.Recognizer()

# 讀取音頻文件
audio_file = sr.AudioFile('audio.wav')
print("Reading the AudioFile....")

# 將音頻文件加載到Recognizer中
with audio_file as source:
    audio = r.record(source)
print("Loading the file into Recognizer....")


# 識別音頻文件中的語音
try:
    text = r.recognize_google(audio, language='zh-TW') # 這裏選擇繁体中文，可以根據需要更改語言
    print("識別结果： " + text)
except sr.UnknownValueError:
    print("無法識別音頻文件中的語音。")
except sr.RequestError as e:
    print("無法從Google API獲取结果； {0}".format(e))
