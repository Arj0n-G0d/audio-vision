from dask import delayed
import numpy as np
import librosa as lb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml
import os

with open("config.yaml") as file :
    config = yaml.safe_load(file)

hopLength = config["preprocessing"]["hopLength"]
melSpectrogramsFolder = config["preprocessing"]["melSpectrogramsFolder"]

@delayed
def convertAudioFileToMelSpectrogram(audioFilePath, melSpectrogramFilePath) :
    print(f"🎵 Processing: {os.path.basename(audioFilePath)}")

    y, sr = lb.load(audioFilePath, sr=None) 
    S = lb.feature.melspectrogram(y=y, sr=sr, hop_length = hopLength)
    dB_values = lb.power_to_db(S, ref=np.max)  

    plt.figure(figsize=(10, 4))
    lb.display.specshow(dB_values, sr=sr, x_axis='time', y_axis='mel')

    plt.axis("off")
    plt.savefig(melSpectrogramFilePath, bbox_inches='tight', pad_inches=0)

    plt.close()
    print(f"🖼️  Saved: {os.path.basename(melSpectrogramFilePath)}\n")
