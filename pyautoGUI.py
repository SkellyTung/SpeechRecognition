import speech_recognition as sr
import pyautogui

# 語音指令辨識
def recognize_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say a command...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='zh-TW')
        print("你說了: " + text)
    except sr.UnknownValueError:
        print("識別失敗")
        text = ""
