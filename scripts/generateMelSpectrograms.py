import pandas as pd
import numpy as np
import librosa as lb
from pathlib import Path
import matplotlib.pyplot as plt
import yaml
import sys
import os

audioExtensions = (
    ".wav", ".mp3", ".aac", ".flac", ".ogg", ".m4a", ".wma", 
    ".aiff", ".opus", ".amr", ".mid", ".midi", ".mp2"
)
outputFolder = "melSpectograms"

with open("config.yaml") as file :
    config = yaml.safe_load(file)

hopLength = config["preprocessing"]["hopLength"]

def getValidDatasetPath() :
    datasetPath = input("📂 Enter the dataset folder path: ").strip()
    if os.path.isdir(datasetPath) :
            print("✅ Path found!\n")
            return datasetPath
    else :
        print("❌ Invalid path. Exiting... 🚪\n")
        exit()

def findAllAudioFiles(datasetPath) :
    path = Path(datasetPath)
    audioFiles = []
    
    for ext in audioExtensions:
        audioFiles.extend(path.rglob(f"*{ext}"))
    return audioFiles

def createOutputFolder() :
    if not os.path.exists(outputFolder) :
        os.makedirs(outputFolder)

def convertAudioToMelSpectrogram(audioFile) :
    print(f"🎵 Processing: {os.path.basename(audioFile)}")

    y, sr = lb.load(audioFile, sr=None) 
    S = lb.feature.melspectrogram(y=y, sr=sr, hop_length = hopLength)
    dB_values = lb.power_to_db(S, ref=np.max)  

    plt.figure(figsize=(10, 4))
    lb.display.specshow(dB_values, sr=sr, x_axis='time', y_axis='mel')
    
    outputPath = os.path.join(outputFolder, os.path.basename(audioFile).split('.')[0] + "_Spectrogram.png")

    plt.axis("off")
    plt.savefig(outputPath, bbox_inches='tight', pad_inches=0)

    plt.close()
    print(f"🖼️  Saved: {outputPath}\n")

def main() :
    datasetPath = getValidDatasetPath()
    audioFiles = findAllAudioFiles(datasetPath)

    if not len(audioFiles):
        print("🚫 No audio files found in the dataset folder. Exiting... 🚪\n")
        exit()
    
    print(f"🔍 Found {len(audioFiles)} audio files. Starting conversion...\n")
    
    createOutputFolder()

    for audioFile in audioFiles[:10] :
        convertAudioToMelSpectrogram(audioFile)

    print(f'🎉 Conversion completed! Check the {outputFolder} folder for spectrograms ✅\n')


if __name__ == "__main__" :
    main()