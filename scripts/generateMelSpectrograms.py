import os
import yaml
from utils.fileHandling import createMelSpectrogramsFolderForGivenDataset, findAudioFilePaths
from utils.audioToMel import convertAudioFileToMelSpectrogram

with open("config.yaml") as file :
    config = yaml.safe_load(file)

melSpectrogramsFolder = config["preprocessing"]["melSpectrogramsFolder"]

def getValidDatasetPath() :
    datasetPath = input("📂 Enter the dataset folder path: ").strip()
    if os.path.isdir(datasetPath) :
            print("✅ Path found!\n")
            return datasetPath
    else :
        print("❌ Invalid path. Exiting... 🚪\n")
        exit()

def main() :
    datasetPath = getValidDatasetPath()
    datasetName = os.path.basename(datasetPath)
    audioFilePaths = findAudioFilePaths(datasetPath)

    if not len(audioFilePaths):
        print("🚫 No audio files found in the dataset folder. Exiting... 🚪\n")
        exit()
    
    print(f"🔍 Found '{len(audioFilePaths)}' audio files. Starting conversion...\n")
    
    createMelSpectrogramsFolderForGivenDataset(datasetName)

    for audioFilePath in audioFilePaths :
        melSpectrogramFilePath = os.path.join(melSpectrogramsFolder, datasetName, os.path.basename(audioFilePath).split('.')[0] + "_Spectrogram.png")
        convertAudioFileToMelSpectrogram(audioFilePath, melSpectrogramFilePath)

    print(f"🎉 Conversion completed! Check the '{melSpectrogramsFolder}' folder for spectrograms ✅\n")

if __name__ == "__main__" :
    main()