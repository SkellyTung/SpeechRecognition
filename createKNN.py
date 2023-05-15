
import librosa
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# 加載聲音文件，提取Mel頻譜特徵
def extract_feature(file_name):
    y, sr = librosa.load(file_name)
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=40)
    feature = np.mean(mfccs.T, axis=0)
    return feature

# 創建KNN模型，訓練模型
def train_model(features, labels):
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(features, labels)
    return model

# 聲紋辨識
def recognize_voice(file_name, model):
    feature = extract_feature(file_name)
    label = model.predict([feature])[0]
    return label

# 訓練KNN模型
features = []
labels = []
for i in range(10):
    for j in range(10):
        file_name = f"data/recordings/{i}_{j}.wav"
        feature = extract_feature(file_name)
        features.append(feature)
        labels.append(i)
model = train_model(features, labels)

# 聲紋辨識測試
test_file = "data/recordings/3_2.wav"
label = recognize_voice(test_file, model)
print(f"Recognized speaker: {label}")
