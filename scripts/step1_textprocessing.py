import os
import re
from vietnam_number import n2w

prefix = "audiobook1_"
# Specify the path to the input folder
input_folder = f"./{prefix}original_transcript"

# Specify the path for the output folder
output_folder = f"./{prefix}original_transcript/{prefix}processed_transcript"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        # Specify the path for the input text file
        input_file_path = os.path.join(input_folder, filename)

        # Extract the directory and base filename without extension
        base_filename, _ = os.path.splitext(filename)

        # Specify the path for the new processed text file
        output_file_path = os.path.join(output_folder, f"{base_filename}.txt")

        # Read the contents of the text file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()

        # Your existing text processing code
        # Task 1: Lowercase all words
        lowercased_text = input_text.lower()

        # Task 2: Remove all non-letter characters (except numbers, %, and dates)
        # Preserve characters with Vietnamese tone marks
        non_letter_pattern = r'[^a-zA-Z0-9%\/àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]+'
        letters_and_numbers_text = re.sub(non_letter_pattern, ' ', lowercased_text)

        # Task 3: Remove all line breaks
        cleaned_text = re.sub(r'\n', ' ', letters_and_numbers_text)

        # Task 4: Replace numbers with their full form using vietnam_number
        def replace_numbers(match):
            number = match.group(0)
            return n2w(number)

        # Replace numbers with their full form
        expanded_text = re.sub(r'\b\d+\b', replace_numbers, cleaned_text)

        # Task 5: Convert dates
        def replace_date(match):
            date = match.group(0)
            day, month, year = date.split('/')
            
            day_text = n2w(day)  # Convert day to written form using vietnam_number
            month_text = [
                'tháng một', 'tháng hai', 'tháng ba', 'tháng tư', 'tháng năm', 'tháng sáu',
                'tháng bảy', 'tháng tám', 'tháng chín', 'tháng mười', 'tháng mười một', 'tháng mười hai'
            ][int(month) - 1]  # Choose the month text
            year_text = 'năm ' + n2w(year)  # Convert year to written form using vietnam_number
            
            return f'ngày {day_text} {month_text} {year_text}'

        # Replace dates with the desired format
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        expanded_text = re.sub(date_pattern, replace_date, expanded_text)

        # Task 6: Add a space between numbers and "%" symbols
        expanded_text = re.sub(r'%', r' phần trăm', expanded_text)


        # Save the processed text into a new file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(expanded_text)
