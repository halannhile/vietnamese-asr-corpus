import os
from praatio import tgio

def update_textgrid_with_single_interval(textgrid_path, transcript_path, output_path):
    # Read the transcript text
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read().strip()

    # Read the original TextGrid file
    tg = tgio.openTextgrid(textgrid_path)

    # Create a new tier with a single interval that covers the whole duration
    new_tier = tgio.IntervalTier('speech', [(0, tg.tierDict[tg.tierNameList[0]].entryList[-1][1], transcript)], 0, tg.tierDict[tg.tierNameList[0]].entryList[-1][1])

    # Replace or add the new tier
    if 'speech' in tg.tierNameList:
        tg.replaceTier('speech', new_tier)
    else:
        tg.addTier(new_tier)

    # Save the updated TextGrid
    tg.save(output_path)

# Set your directories here

prefix = "audiobook1_"

textgrid_directory = f'./{prefix}split_textgrid'
transcript_directory = f'./{prefix}original_transcript/{prefix}processed_transcript'
output_directory = f'./{prefix}speech_corpus'

# Loop through textgrid files in the textgrid directory and update TextGrids
for textgrid_file in os.listdir(textgrid_directory):
    if textgrid_file.endswith('.TextGrid'):
        base_name = os.path.splitext(textgrid_file)[0]
        textgrid_path = os.path.join(textgrid_directory, textgrid_file)
        transcript_path = os.path.join(transcript_directory, f"{base_name}.txt")
        output_path = os.path.join(output_directory, f"{base_name}.TextGrid")
        update_textgrid_with_single_interval(textgrid_path, transcript_path, output_path)
