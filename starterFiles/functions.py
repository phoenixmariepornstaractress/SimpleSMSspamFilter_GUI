# Improved and Modular SMS Spam Filter GUI

# Imports
from dearpygui.core import *
from dearpygui.simple import *
import pandas as pd
import string
import nltk
import datetime
import os
from collections import Counter

# NLTK Data Download
nltk.download('punkt')
nltk.download('stopwords')

# Constants
DATA_FILE = 'SMSSpamCollection.txt'
LOGO_IMAGE = 'logo_spamFilter.png'

# Load dataset
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Required file '{DATA_FILE}' not found.")

data = pd.read_csv(DATA_FILE, sep='\t', header=None, names=['label', 'sms'])

# Preprocessing
stop_words = set(nltk.corpus.stopwords.words('english'))
def pre_process(text):
    text = ''.join([char.lower() for char in text if char not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    return [word for word in tokens if word not in stop_words]

data['processed'] = data['sms'].apply(pre_process)

# Word Categorization
def categorize_words():
    spam_words = [word for sms in data['processed'][data['label'] == 'spam'] for word in sms]
    ham_words = [word for sms in data['processed'][data['label'] == 'ham'] for word in sms]
    return spam_words, ham_words

spam_words, ham_words = categorize_words()

# Prediction
COLOR_SPAM = [220, 50, 50]
COLOR_HAM = [100, 220, 50]
COLOR_UNKNOWN = [255, 255, 255]

def predict(input_words):
    spam_score = sum(spam_words.count(word) for word in input_words)
    ham_score = sum(ham_words.count(word) for word in input_words)
    total = spam_score + ham_score

    if total == 0:
        return "message could be spam, with 50% certainty", COLOR_UNKNOWN

    certainty = round((max(spam_score, ham_score) / total) * 100, 2)
    if spam_score > ham_score:
        return f"message is spam, with {certainty}% certainty", COLOR_SPAM
    else:
        return f"message is not spam, with {certainty}% certainty", COLOR_HAM

# Summary & Analysis
def get_summary(words):
    return {
        "word_count": len(words),
        "unique_words": len(set(words)),
        "spam_score": round(100 * len([w for w in words if w in spam_words]) / len(words), 2) if words else 0,
        "frequent_words": Counter(words).most_common(5)
    }

def show_summary(words):
    summary = get_summary(words)
    add_spacing(4)
    add_text(f"Word Count: {summary['word_count']}", color=[100, 100, 255])
    add_text(f"Unique Words: {summary['unique_words']}", color=[100, 255, 100])
    add_text(f"Spam Score: {summary['spam_score']}%", color=[255, 165, 0])
    add_text("Most Frequent Words:", color=[0, 191, 255])
    for word, freq in summary['frequent_words']:
        add_text(f"- {word}: {freq} times", bullet=True)

# Input/Output Utilities
def clear_input():
    set_value("Input", "")

def save_input():
    with open("saved_input.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] {get_value('Input')}\n")

def export_summary():
    words = pre_process(get_value("Input"))
    summary = get_summary(words)
    with open("summary_report.txt", "a") as f:
        f.write("Summary Report\n====================\n")
        f.write(f"Word Count: {summary['word_count']}\n")
        f.write(f"Unique Words: {summary['unique_words']}\n")
        f.write(f"Spam Score: {summary['spam_score']}%\n")
        f.write("Most Frequent Words:\n")
        for word, count in summary['frequent_words']:
            f.write(f"- {word}: {count} times\n")
        f.write("\n")

def show_dataset_stats():
    with window("Dataset Summary", width=480, height=250):
        total = len(data)
        spam_total = len(data[data['label'] == 'spam'])
        ham_total = len(data[data['label'] == 'ham'])
        add_text("Dataset Stats", color=[255, 255, 0])
        add_text(f"Total Messages: {total}")
        add_text(f"Spam: {spam_total} ({round(100*spam_total/total,2)}%)")
        add_text(f"Ham: {ham_total} ({round(100*ham_total/total,2)}%)")
        add_text(f"Unique Words: {len(set(spam_words + ham_words))}")

def show_help():
    with window("Help", width=460, height=220):
        add_text("How to Use the SMS Spam Filter", color=[255, 255, 102])
        add_text("- Enter an SMS message in the input box.")
        add_text("- Click 'Check' to analyze.")
        add_text("- Use buttons below to clear, save, or export.")
        add_text("- View dataset insights or get help anytime.")

# Callback

def check_message_callback(sender, data):
    message = get_value("Input")
    words = pre_process(message)
    result, color = predict(words)
    with window("SMS Spam Filter Result"):
        add_text(result, color=color)
        show_summary(words)

# GUI Setup
set_main_window_size(560, 770)
set_theme("Gold")
set_global_font_scale(1.25)

with window("SMS Spam Filter", width=540, height=750):
    set_window_pos("SMS Spam Filter", 0, 0)
    add_drawing("Logo", width=520, height=240)
    add_text("Enter an SMS message to check if it's spam.", color=[232, 163, 33])
    add_input_text("Input", width=480, default_value="Type message here!")
    add_button("Check", callback=check_message_callback)
    add_spacing(count=4)
    add_button("Clear Input", callback=clear_input)
    add_button("Save Input", callback=save_input)
    add_button("Export Summary", callback=export_summary)
    add_button("Show Dataset Stats", callback=show_dataset_stats)
    add_button("Help", callback=show_help)

draw_image("Logo", LOGO_IMAGE, [0, 240])

start_dearpygui()
print("GUI Closed")
