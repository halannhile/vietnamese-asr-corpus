from praatio import tgio
import soundfile as sf
from auditok import split
import os

prefix = "audiobook1_"

# Specify the path to the input folder
input_folder = f"./{prefix}speech_corpus"

# Create directories for the corresponding output locations
output_directory_1 = f"./{prefix}speech_corpus"
output_directory_2 = f"./{prefix}split_textgrid"
os.makedirs(output_directory_1, exist_ok=True)
os.makedirs(output_directory_2, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".wav"):
        # Specify the path for the input wav file
        input_wav_path = os.path.join(input_folder, filename)

        # Load the wave signal and sample rate
        wav, sr = sf.read(input_wav_path)

        # Split region into speech segments
        energy_threshold = 10
        region = split(input_wav_path, energy_threshold=energy_threshold)

        # Duration in seconds
        duration = len(wav) / sr

        # Initialize a blank Textgrid object for the first location
        tg_1 = tgio.Textgrid()
        entryList_1 = []

        # Initialize a blank Textgrid object for the second location
        tg_2 = tgio.Textgrid()
        entryList_2 = []

        # Iterate through the region to get starts and ends of elements (speech segments) and annotate
        for elt in region:
            start, end = elt.meta.start, elt.meta.end

            # For the first location
            entry_1 = tgio.Interval(start, end, "*")
            entryList_1.append(entry_1)

            # For the second location
            entry_2 = tgio.Interval(start, end, "*")
            entryList_2.append(entry_2)

        # "str": name of IntervalTier, 0 - duration: covering the entire duration of the audio
        tier_1 = tgio.IntervalTier("words", entryList_1, 0, duration)
        tg_1.addTier(tier_1)

        tier_2 = tgio.IntervalTier("words", entryList_2, 0, duration)
        tg_2.addTier(tier_2)

        # Save the TextGrid for the current wav file to the first location
        output_textgrid_1 = os.path.join(output_directory_1, f"{os.path.splitext(filename)[0]}.TextGrid")
        tg_1.save(output_textgrid_1)

        # Save the TextGrid for the current wav file to the second location
        output_textgrid_2 = os.path.join(output_directory_2, f"{os.path.splitext(filename)[0]}.TextGrid")
        tg_2.save(output_textgrid_2)
