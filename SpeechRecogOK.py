import pyaudio
import wave
import speech_recognition as sr
import os
import numpy as np


# 獲取當前檔案的路徑 test
# 在程式碼的開頭使用__file__變數來獲取當前檔案的路徑，然後搭配os.path模組中的函數來處理路徑，以獲取"audio.wav"和"model.onnx"的完整路徑。
current_path = os.path.dirname(os.path.abspath(__file__))



# 配置錄音參數
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = os.path.join(current_path, "audio.wav")  # 完整的音訊檔案路徑

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
print("Finish Record and Stop Stream...")

# 保存錄音文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
print("Saving the Record...")


# 創建Recognizer對象
r = sr.Recognizer()

# 讀取音頻文件
audio_file = sr.AudioFile(os.path.join(current_path, "audio.wav"))  # 完整的音訊檔案路徑
print("Reading the AudioFile...")

# 將音頻文件加載到Recognizer中
with audio_file as source:
    audio = r.record(source)
print("Loading the file into Recognizer...")


# 識別音頻文件中的語音
try:
    text = r.recognize_google(audio, language='zh-TW') # 這裏選擇繁体中文，可以根據需要更改語言
    print("識別结果： " + text)
except sr.UnknownValueError:
    print("無法識別音頻文件中的語音。")
except sr.RequestError as e:
    print("無法從Google API獲取结果； {0}".format(e))


# 將Python程式碼轉換為ONNX模型檔案
import onnx
from onnx import helper, TensorProto, numpy_helper

# ...

# 將Python程式碼轉換為ONNX模型檔案

# 創建計算圖
graph = helper.make_graph(
    nodes=[],
    name="speech_recognition",
    inputs=[],
    outputs=[],
    initializer=[],
)

# 輸入
input_name = "input"
input_shape = (1, 16000)
input_type = onnx.TensorProto.FLOAT

input_tensor = helper.make_tensor_value_info(
    name=input_name,
    elem_type=input_type,
    shape=input_shape
)

graph.input.extend([input_tensor])

# 輸出
output_name = "output"
output_shape = (1,)
output_type = onnx.TensorProto.STRING

output_tensor = helper.make_tensor_value_info(
    name=output_name,
    elem_type=output_type,
    shape=output_shape
)

graph.output.extend([output_tensor])

# 初始化器
initializer = [
    numpy_helper.from_array(np.random.randn(3, 3, 1, 32).astype(np.float32), name='weight'),
    numpy_helper.from_array(np.zeros(32, dtype=np.float32), name='bias')
]

graph.initializer.extend(initializer)

# 創建ONNX模型
model = helper.make_model(graph, producer_name='speech_recognition')

# 將模型保存為ONNX檔案
onnx_file_path = os.path.join(current_path, "speech_recognition.onnx")
onnx.save_model(model, onnx_file_path)

print("Conversion to ONNX is completed. The ONNX model is saved at: " + onnx_file_path)
