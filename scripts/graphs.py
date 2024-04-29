import os
import streamlit as st

def count_words_in_files(folder_path):
    word_counts = {}
    total_word_count = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    words = file.read().split()
                    count = len(words)
                    word_counts[file_name] = count
                    total_word_count += count
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
    return word_counts, total_word_count

def display_word_count_graph(folder_path):
    word_counts, total_word_count = count_words_in_files(folder_path)
    if word_counts:
        st.write("Word Count per File")
        st.bar_chart(data=word_counts)
        st.write(f"Total Word Count: {total_word_count}")
    else:
        st.write("No text files found or an error occurred.")
