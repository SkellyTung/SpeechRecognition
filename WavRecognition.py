import speech_recognition as sr

# 創建Recognizer對象
r = sr.Recognizer()

# 讀取音頻文件
audio_file = sr.AudioFile('audio.wav')

# 將音頻文件加載到Recognizer中
with audio_file as source:
    audio = r.record(source)

# 識別音頻文件中的語音
try:
    text = r.recognize_google(audio, language='zh-TW') # 這裏選擇繁体中文，可以根據需要更改語言
    print("識別结果： " + text)
except sr.UnknownValueError:
    print("無法識別音頻文件中的語音。")
except sr.RequestError as e:
    print("無法從Google API獲取结果； {0}".format(e))
