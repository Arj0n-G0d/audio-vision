import pandas as pd
from pathlib import Path
import os
import yaml

with open("config.yaml") as file :
    config = yaml.safe_load(file)

audioExtensions = config["preprocessing"]["audioExtensions"]
melSpectrogramsFolder = config["preprocessing"]["melSpectrogramsFolder"]
dirPath = config["paths"]["audioData"]
csvPath = os.path.join(dirPath, "dataset.csv")

def createMelSpectrogramsFolderForGivenDataset(datasetName) :
    if not os.path.exists(melSpectrogramsFolder) :
        os.makedirs(melSpectrogramsFolder)
    
    if not os.path.exists(os.path.join(melSpectrogramsFolder, datasetName)) :
        os.makedirs(os.path.join(melSpectrogramsFolder, datasetName))

    df = pd.read_csv(csvPath)
    classes = df["class"].unique()

    for className in classes :
        if not os.path.exists(os.path.join(melSpectrogramsFolder, datasetName, className)) :
            os.makedirs(os.path.join(melSpectrogramsFolder, datasetName, className))
