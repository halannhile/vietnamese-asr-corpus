from praatio import tgio
import soundfile as sf
import os

prefix = "audiobook1_"

# Define the paths to the TextGrid and WAV files
textgrid_folder = f"./{prefix}combined_textgrid/"
wav_folder = f"./{prefix}speech_corpus/"
output_folder = f"./{prefix}asr_corpus/"


# Iterate through files in the split_textgrid_folder
for filename in os.listdir(textgrid_folder):
    if filename.endswith(".TextGrid"):

         # Define the path to the input TextGrid
        input_textgrid_path =  os.path.join(textgrid_folder, filename)

        # Extract the base filename (without extension) from the WAV file
        base_filename = os.path.splitext(os.path.basename(input_textgrid_path))[0]

         # Define the path to the input eav
        input_wav_path =  os.path.join(wav_folder, f"{base_filename}.wav")

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Load the TextGrid
        textgrid = tgio.openTextgrid(input_textgrid_path)

        # Load the WAV file and its sample rate
        wav_data, sample_rate = sf.read(input_wav_path)

        # Initialize segment counter
        segment_counter = 1

        # Iterate through intervals in the TextGrid
        for tier_name in textgrid.tierNameList:
            tier = textgrid.tierDict[tier_name]

            for interval in tier.entryList:
                start_time = interval[0]
                end_time = interval[1]
                transcription = interval[2]

                # Check if the interval is non-empty and at least 2 seconds
                if transcription.strip() and end_time - start_time >= 2.0:
                    # Extract the segment from the WAV data
                    start_sample = int(start_time * sample_rate)
                    end_sample = int(end_time * sample_rate)
                    segment = wav_data[start_sample:end_sample]

                    # Define the filenames for the segment within the subfolder
                    wav_filename = os.path.join(output_folder, f"{base_filename}_segment{segment_counter}.wav")
                    txt_filename = os.path.join(output_folder, f"{base_filename}_segment{segment_counter}.txt")

                    # Save the segment as a WAV file
                    sf.write(wav_filename, segment, sample_rate)

                    # Save the transcription as a text file
                    with open(txt_filename, "w", encoding="utf-8") as txt_file:
                        txt_file.write(transcription)

                    segment_counter += 1