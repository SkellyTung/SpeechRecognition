import speech_recognition as sr
import time
import pyaudio

# 初始化语音识别器对象
r = sr.Recognizer()

# 初始化麦克风输入
with sr.Microphone() as source:
    print("請說出指令...")
    audio = r.listen(source)

    # 使用Google語音識別API識別語音
    try:
        text = r.recognize_google(audio, language='zh-TW')
        print("你說了: " + text)
    except sr.UnknownValueError:
        print("識別失敗")
        text = ""

    # 根據指令控制電梯開關門
    if "開門" in text:
        # 控制电梯开门
        print("正在打開電梯門...")
        time.sleep(3) # 模拟电梯门开启的时间
        print("電梯門已經打開")
    elif "關門" in text:
        # 控制电梯关门
        print("正在關閉電梯門...")
        time.sleep(3) # 模拟电梯门关闭的时间
        print("電梯門已經關閉")
    else:
        print("不是有效指令")

