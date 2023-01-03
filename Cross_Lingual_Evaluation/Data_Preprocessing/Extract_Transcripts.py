import os
import pandas as pd
import whisper
pd.options.display.max_rows = 100

def extract_speech_transcripts(path_to_recordings, output_folder):

    """Extract speech transcripts"""
    paths = [os.path.join(path_to_recordings, base) for base in os.listdir(path_to_recordings)]

    # keep only non-empty recordings (> 56 Bytes)
    files = []
    for m in paths:
        size = os.stat(m).st_size/1000
        if size > 56:
            files.append(m)

    # extract and save transcripts.
    for i in files:
        #print(i)
        model = whisper.load_model("medium")
        result = model.transcribe(i)
        test = result['text']
        base = os.path.basename(i).split(".wav")[0]
        total = os.path.join(output_folder, base + ".txt")
        text_file = open(total, "wt")
        n = text_file.write(test)
        text_file.close()

    

