import os
import yaml
from pathlib import Path

with open("config.yaml") as file :
    config = yaml.safe_load(file)

audioExtensions = config["preprocessing"]["audioExtensions"]
melSpectrogramsFolder = config["preprocessing"]["melSpectrogramsFolder"]

def findAudioFilePaths(datasetPath) :
    path = Path(datasetPath)
    audioFilePaths = []
    
    for ext in audioExtensions:
        audioFilePaths.extend(path.rglob(f"*{ext}"))
    return audioFilePaths

def createMelSpectrogramsFolderForGivenDataset(datasetName) :
    if not os.path.exists(melSpectrogramsFolder) :
        os.makedirs(melSpectrogramsFolder)
    
    if not os.path.exists(os.path.join(melSpectrogramsFolder, datasetName)) :
        os.makedirs(os.path.join(melSpectrogramsFolder, datasetName))
    
