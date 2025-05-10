from dearpygui.core import *
from dearpygui.simple import *

import re
import string
import datetime

# Global list to keep prediction history
predictions = []

# --- Text Processing Utilities ---
def pre_process(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub("\d+", "", text)
    text = " ".join(text.split())
    return text

def categorize_words(text):
    return text.split()

def count_words(text):
    return len(text.split())

def extract_unique_words(text):
    return list(set(text.split()))

def calculate_spam_score(text):
    spam_keywords = ["free", "winner", "win", "cash", "prize", "buy", "urgent"]
    words = text.split()
    matches = [word for word in words if word in spam_keywords]
    score = len(matches) / len(words) if words else 0
    return round(score * 100, 2)

def get_most_frequent_words(text, n=5):
    words = text.split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]

# --- Prediction Logic ---
def predict(text):
    spam_keywords = ["free", "winner", "win", "cash", "prize", "buy", "urgent"]
    if any(word in text for word in spam_keywords):
        return ("Spam", [255, 0, 0])
    else:
        return ("Not Spam", [0, 128, 0])

# --- Reporting Functions ---
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

# --- Button Callback Functions ---
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
    summary = get_message_summary(pre_process(input_value))
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

def check_spam_callback(sender, data):
    input_value = get_value("Input")
    processed_input = pre_process(input_value)
    prediction, color = predict(processed_input)
    predictions.append(prediction)

    # Clear any previous prediction display
    if len(predictions) > 1:
        hide_item(predictions[-2])

    with window("Simple SMS Spam Filter"):
        add_spacing(count=12)
        add_separator()
        add_spacing(count=12)
        add_text(prediction, color=color)
        display_word_info(processed_input)

# --- GUI Setup ---
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
