from utils.fileHandling import createMelSpectrogramsFolderForGivenDataset
from utils.audioPreprocessing import convertAudioFileToMelSpectrogram
import pandas as pd
import os
import yaml
import dask

batchSize = 2

with open("config.yaml") as file :
    config = yaml.safe_load(file)

melSpectrogramsFolder = config["preprocessing"]["melSpectrogramsFolder"]
dirPath = config["paths"]["audioData"]
csvPath = os.path.join(dirPath, "dataset.csv")

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

    if not os.path.exists(csvPath):
        print('🚫 No "dataset.csv" found in the dataset folder. Exiting... 🚪\n')
        exit()

    df = pd.read_csv(csvPath)

    print(f"🔍 Found '{len(df)}' audio files. Starting conversion...\n")
    
    createMelSpectrogramsFolderForGivenDataset(datasetName)

    tasks = []
    for i in range(len(df)) :
        melSpectrogramFilePath = os.path.join(melSpectrogramsFolder, datasetName, df.loc[i]["class"], os.path.basename(df.loc[i]["audio_file_path"]).split('.')[0] + "_Spectrogram.png")
        tasks.append(convertAudioFileToMelSpectrogram(df.loc[i]["audio_file_path"], melSpectrogramFilePath))

    # scheduler determines the type of parallel execution (threads, processes, distributed, or sync)
    # num_workers = Number of threads to use
    dask.compute(tasks, scheduler = "processes", num_workers = 16)

    print(f"🎉 Conversion completed! Check the '{melSpectrogramsFolder}' folder for spectrograms ✅\n")

if __name__ == "__main__" :
    main()