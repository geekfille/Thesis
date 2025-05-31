# Install and import
!pip install hazm

import os
import re
import string
import pandas as pd
from hazm import HamshahriReader, word_tokenize, Normalizer

from google.colab import drive
drive.mount('/content/drive')

# Shared search pattern
SEARCH_PATTERN = r'\b(?:از|ز|ب|بر|در|و|را|رو|با|-)?دس(:?ت)?(?:ها|های|ای|ا|ان)?(?:م|ت|ش|مان|تان|شان|مون|تون|شون)?\b'

# Concordance generator
def generate_concordance(tokens, pattern, left_col, right_col):
    for i, token in enumerate(tokens):
        if re.match(pattern, token):
            start_index = max(0, i - left_col)
            end_index = min(len(tokens), i + right_col + 1)
            concordance_tokens = tokens[start_index:end_index]

            key_word_position = i - start_index
            row = {'L{}'.format(key_word_position - j): conc_token 
                   for j, conc_token in enumerate(reversed(concordance_tokens[:key_word_position]))}
            row['Key Word'] = token
            row.update({'R{}'.format(j + 1): conc_token 
                        for j, conc_token in enumerate(concordance_tokens[key_word_position + 1:])})
            yield row

# General corpus processor
def process_corpus(texts, pattern, output_path):
    normalizer = Normalizer()
    normalized_texts = normalizer.normalize(texts)
    tokens = word_tokenize(normalized_texts)

    concordance_lines = list(generate_concordance(tokens, pattern, 15, 15))
    df = pd.DataFrame(concordance_lines)
    df.to_excel(output_path, index=False)

# Hamshahri corpus
def process_hamshahri():
    data_path = "/content/drive/MyDrive/Hamshahri/input/Random_Sample_5"
    hamshahri = HamshahriReader(root=data_path)
    h_texts = " ".join(text for text in hamshahri.texts())

    output_path = '/content/drive/MyDrive/output/ham_dast_160_all_data.xlsx'
    process_corpus(h_texts, SEARCH_PATTERN, output_path)

# Dastan corpus
def merge_text_files(folder_path):
    merged_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                merged_text += f.read() + "\n"
    return merged_text

def process_dastan():
    d_folder_path = "/content/drive/MyDrive/Dastan/input/All"
    d_texts = merge_text_files(d_folder_path)

    # Normalize encoding and digits
    d_texts = d_texts.replace('ك', 'ک').replace('ي', 'ی').replace("\ufeff", "").replace('\u00A0', " ")
    d_texts = re.sub(r'[\u064b-\u0652]', '', d_texts)
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    arabic_digits = '0123456789'
    d_texts = d_texts.translate(str.maketrans(persian_digits, arabic_digits))

    output_path = '/content/drive/MyDrive/output/das_dast_all_data.xlsx'
    process_corpus(d_texts, SEARCH_PATTERN, output_path)

# Run both
process_hamshahri()
process_dastan()


