from praatio import tgio
import os

prefix = "audiobook1_"

# Specify the input and output folders
split_textgrid_folder = f"./{prefix}split_textgrid/"
aligned_textgrid_folder = f"./{prefix}mfa_aligned_textgrid/"
combined_textgrid_folder = f"./{prefix}combined_textgrid/"

# Iterate through files in the split_textgrid_folder
for filename in os.listdir(split_textgrid_folder):
    if filename.endswith(".TextGrid"):

        # Define the path to the input TextGrid
        input_textgrid_path =  os.path.join(aligned_textgrid_folder, filename)

        # Load the TextGrid with individual words
        word_tg = tgio.openTextgrid(input_textgrid_path)

        # Construct the path to the segmented speech TextGrid with the same base filename and energy_threshold
        speech_textgrid_path = os.path.join(split_textgrid_folder, filename)

        # Load the TextGrid with segmented speech regions
        speech_tg = tgio.openTextgrid(speech_textgrid_path)

        # Extract the base filename (without extension) from the input TextGrid path
        base_filename = os.path.splitext(os.path.basename(input_textgrid_path))[0]

        # Create the output folder if it doesn't exist
        os.makedirs(combined_textgrid_folder, exist_ok=True)

        # Construct the output TextGrid path with the same filename
        output_textgrid_path = os.path.join(combined_textgrid_folder, f"{base_filename}.TextGrid")

        # Create a new TextGrid to store the combined information
        combined_tg = tgio.Textgrid()

        # Copy the minimum and maximum timestamps from the segmented speech TextGrid
        combined_tg.minTimestamp = speech_tg.minTimestamp
        combined_tg.maxTimestamp = speech_tg.maxTimestamp

        # Initialize a list to store the entries for the new TextGrid
        new_entries = []

        # Iterate through intervals in the segmented speech TextGrid
        for speech_interval in speech_tg.tierDict["words"].entryList:
            speech_start = speech_interval[0]
            speech_end = speech_interval[1]

            # Convert speech_start and speech_end to float
            speech_start_float = float(speech_start)
            speech_end_float = float(speech_end)

            # Find words that fall within the speech segment
            words_in_segment = []
            for word_interval in word_tg.tierDict["words"].entryList:
                word_start = float(word_interval[0])
                word_end = float(word_interval[1])

                # Check if the word_interval overlaps with the speech segment
                if speech_start_float <= word_end and speech_end_float >= word_start:
                    words_in_segment.append(word_interval[2])

            # Combine words into a single string
            combined_words = " ".join(words_in_segment)

            # Create a new entry for the combined TextGrid
            new_entry = tgio.Interval(speech_start, speech_end, combined_words)
            new_entries.append(new_entry)

        # Create a new tier in the combined TextGrid
        combined_tier = tgio.IntervalTier("speech_segments", new_entries, combined_tg.minTimestamp, combined_tg.maxTimestamp)

        # Add the new tier to the combined TextGrid
        combined_tg.addTier(combined_tier)

        # Save the combined TextGrid with the same filename as the input TextGrid
        combined_tg.save(output_textgrid_path)
