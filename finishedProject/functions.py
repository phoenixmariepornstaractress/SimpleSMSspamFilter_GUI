# SMS Spam Filter GUI - Enhanced Version

# Imports
from dearpygui.core import *
from dearpygui.simple import *
import random
import pandas as pd
import string
import nltk
import datetime
from collections import Counter
nltk.download('punkt')
nltk.download('stopwords')

# Load and preprocess data
data = pd.read_csv('SMSSpamCollection.txt', sep='\t', header=None, names=["label", "sms"])

# Pre-processing function
def pre_process(sms):
    remove_punct = "".join([char.lower() for char in sms if char not in string.punctuation])
    tokenize = nltk.tokenize.word_tokenize(remove_punct)
    remove_stop_words = [word for word in tokenize if word not in nltk.corpus.stopwords.words('english')]
    return remove_stop_words

data['processed'] = data['sms'].apply(pre_process)

# Categorize words
spam_words = []
ham_words = []
for sms in data['processed'][data['label'] == 'spam']:
    spam_words.extend(sms)
for sms in data['processed'][data['label'] == 'ham']:
    ham_words.extend(sms)

# Predict function with confidence
def predict(user_input):
    spam_counter = sum(spam_words.count(word) for word in user_input)
    ham_counter = sum(ham_words.count(word) for word in user_input)
    red = [220, 50, 50]
    green = [100, 220, 50]

    if ham_counter > spam_counter:
        certainty = round((ham_counter / (ham_counter + spam_counter)) * 100, 2)
        return f"message is not spam, with {certainty}% certainty", green
    elif spam_counter > ham_counter:
        certainty = round((spam_counter / (ham_counter + spam_counter)) * 100, 2)
        return f"message is spam, with {certainty}% certainty", red
    else:
        return "message could be spam, with 50% certainty", [255, 255, 255]

# Analytics functions
def count_words(text):
    return len(text)

def extract_unique_words(text):
    return list(set(text))

def calculate_spam_score(text):
    spam_matches = [word for word in text if word in spam_words]
    score = len(spam_matches) / len(text) if text else 0
    return round(score * 100, 2)

def get_most_frequent_words(text, n=5):
    freq = Counter(text)
    return freq.most_common(n)

def get_message_summary(text):
    return {
        "word_count": count_words(text),
        "unique_count": len(extract_unique_words(text)),
        "spam_score": calculate_spam_score(text),
        "frequent_words": get_most_frequent_words(text)
    }

def display_word_info(text):
    summary = get_message_summary(text)
    add_spacing(count=8)
    add_text(f"Word Count: {summary['word_count']}", color=[100, 100, 255])
    add_spacing(count=4)
    add_text(f"Unique Words: {summary['unique_count']}", color=[100, 255, 100])
    add_spacing(count=4)
    add_text(f"Spam Score: {summary['spam_score']}%", color=[255, 165, 0])
    add_spacing(count=4)
    add_text("Most Frequent Words:", color=[0, 191, 255])
    for word, count in summary['frequent_words']:
        add_text(f"- {word}: {count} times", bullet=True)

# Additional functionalities
def display_spam_ham_ratios():
    total_spam = len(data[data['label'] == 'spam'])
    total_ham = len(data[data['label'] == 'ham'])
    ratio_text = f"Total Messages - Spam: {total_spam}, Ham: {total_ham}"
    add_spacing(count=6)
    add_text(ratio_text, color=[128, 0, 128])

def show_random_example():
    example = data.sample(1).iloc[0]
    msg_type = example['label'].capitalize()
    add_spacing(count=6)
    add_text(f"Random Example ({msg_type}):", color=[0, 100, 200])
    add_text(example['sms'], wrap=450)

# Utility functions
def clear_input():
    set_value("Input", "")
    log_info("Input cleared.")

def save_input_to_file():
    input_value = get_value("Input")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("saved_input.txt", "a") as f:
        f.write(f"[{timestamp}] {input_value}\n")
    log_info("Input saved to file.")

def export_summary():
    input_value = get_value("Input")
    processed_input = pre_process(input_value)
    summary = get_message_summary(processed_input)
    with open("summary_report.txt", "a") as f:
        f.write("Summary Report\n")
        f.write("==============\n")
        f.write(f"Word Count: {summary['word_count']}\n")
        f.write(f"Unique Words: {summary['unique_count']}\n")
        f.write(f"Spam Score: {summary['spam_score']}%\n")
        f.write("Most Frequent Words:\n")
        for word, count in summary['frequent_words']:
            f.write(f"- {word}: {count} times\n")
        f.write("\n")
    log_info("Summary exported to file.")

# Main check button callback
def check_spam_callback(sender, data):
    input_value = get_value("Input")
    processed_input = pre_process(input_value)
    prediction, color = predict(processed_input)
    with window("Simple SMS Spam Filter"):
        add_spacing(count=12)
        add_separator()
        add_spacing(count=12)
        add_text(prediction, color=color)
        display_word_info(processed_input)
        display_spam_ham_ratios()
        show_random_example()

# GUI setup
set_main_window_size(540, 720)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30, 30)

with window("Simple SMS Spam Filter", width=520, height=677):
    set_window_pos("Simple SMS Spam Filter", 0, 0)
    add_drawing("logo", width=520, height=290)
    add_separator()
    add_spacing(count=12)
    add_text("Please enter an SMS message of your choice to check if it's spam or not", color=[232, 163, 33])
    add_spacing(count=12)
    add_input_text("Input", width=415, default_value="type message here!")
    add_spacing(count=12)
    add_button("Check", callback=check_spam_callback)
    add_spacing(count=6)
    add_button("Clear Input", callback=clear_input)
    add_spacing(count=6)
    add_button("Save Input", callback=save_input_to_file)
    add_spacing(count=6)
    add_button("Export Summary", callback=export_summary)

draw_image("logo", "logo_spamFilter.png", [0, 240])

start_dearpygui()
print("Bye Bye, GUI")
 
