!pip install hazm

import os
import string
from hazm import HamshahriReader, word_tokenize, Normalizer
import re
import pandas as pd
import random

from google.colab import drive
drive.mount('/content/drive')

#Hamshahri
data = "/content/drive/MyDrive/Hamshahri/input/Random_Sample_5"
hamshahri = HamshahriReader(root = data)
h_texts = " ".join(text for text in hamshahri.texts())


normalizer = Normalizer()
h_texts = normalizer.normalize(h_texts)
h_tokens = word_tokenize(h_texts)

def generate_concordance(tokens, pattern, left_col, right_col):
    for i, token in enumerate(tokens):
        if re.match(pattern, token):
            start_index = max(0, i - left_col)
            end_index = min(len(tokens), i + right_col + 1)
            concordance_tokens = tokens[start_index:end_index]

            key_word_position = left_col
            row = {'L{}'.format(left_col - j): conc_token for j, conc_token in enumerate(reversed(concordance_tokens[key_word_position+1:]))}
            row['Key Word'] = token
            row.update({'R{}'.format(right_col - j): conc_token for j, conc_token in enumerate(reversed(concordance_tokens[:key_word_position]))})
            yield row

# Define your regex pattern
search_pattern = r'\b(?:از|ز|ب|بر|در|و|را|رو|با|-)?دندون(?:ها|های|ای|ا)?(?:م|ت|ش|مان|تان|شان|مون|تون|شون)?\b'

all_concordance_lines = list(generate_concordance(h_tokens, search_pattern, 15, 15))

# Save all concordance lines to Excel before sampling
df_all = pd.DataFrame(all_concordance_lines)
# Define the output Excel file path for the full data
full_excel_file_path = '/content/drive/MyDrive/output/ham_dandun_160_all_data.xlsx'
df_all.to_excel(full_excel_file_path, index=False)


#DASTAN
def merge_text_files(folder_path):
    merged_text = ""

    # Traverse the directory tree
    for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    merged_text += f.read() + "\n"

    return merged_text


# Define the root folder containing subfolders with .txt files
d_folder_path = "/content/drive/MyDrive/Dastan/input/All"

# Merge all text files
d_texts = merge_text_files(d_folder_path)
d_texts = d_texts.replace('ك', 'ک').replace('ي', 'ی').replace("\ufeff", "").replace('\u00A0', " ")
d_texts = re.sub(r'[\u064b-\u0652]', '', d_texts)

persian_digits = '۰۱۲۳۴۵۶۷۸۹'
arabic_digits = '0123456789'
trans_table = str.maketrans(persian_digits, arabic_digits)  # or reverse for converting to Persian
d_texts = d_texts.translate(trans_table)

d_tokens = word_tokenize(d_texts)


def generate_concordance(tokens, pattern, left_col, right_col):
    for i, token in enumerate(tokens):
        if re.match(pattern, token):
            start_index = max(0, i - left_col)
            end_index = min(len(tokens), i + right_col + 1)
            concordance_tokens = tokens[start_index:end_index]

            key_word_position = left_col
            row = {'L{}'.format(left_col - j): conc_token for j, conc_token in enumerate(reversed(concordance_tokens[key_word_position+1:]))}
            row['Key Word'] = token
            row.update({'R{}'.format(right_col - j): conc_token for j, conc_token in enumerate(reversed(concordance_tokens[:key_word_position]))})
            yield row

# Define your regex pattern
search_pattern = r'\b(?:از|ز|ب|بر|در|و|را|رو|با|-)?دندون(?:ها|های|ای|ا)?(?:م|ت|ش|مان|تان|شان|مون|تون|شون)?\b'

all_concordance_lines = list(generate_concordance(d_tokens, search_pattern, 15, 15))

# Save all concordance lines to Excel before sampling
df_all = pd.DataFrame(all_concordance_lines)
# Define the output Excel file path for the full data
full_excel_file_path = '/content/drive/MyDrive/output/das_dandun_all_data.xlsx'
df_all.to_excel(full_excel_file_path, index=False)


