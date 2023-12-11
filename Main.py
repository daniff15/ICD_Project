import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Set page title and icon
st.set_page_config(page_title='Gamification Study', page_icon='🎓')

# Define styles
background_color = "#f0f0f0"
text_color = "#333333"
title_font_size = 2  # Relative font size for the title

# Main title with styles
st.markdown(
    f"""
    <h1 style='text-align:center;'>Gamification Enhances Student Motivation?</h1>
    """,
    unsafe_allow_html=True
)

# Load data
DATE_COLUMN = 'Abstract'
DATA_URL = ('./data/icd_scopus.csv')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data

# Display abstract data
def display_abstract_data(data):
    st.subheader('Abstract Data')
    st.write(data['Abstract'])

# Display character frequency plot
def display_character_frequency_plot(data):
    st.subheader('Character Frequency Distribution')

    # Check special characters and punctuation frequency
    char_freq = Counter(data['Abstract'].str.cat())

    # Prepare data for plotting
    char_labels, char_values = zip(*char_freq.items())

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.bar(char_labels, char_values)
    ax.set_xlabel('Characters')
    ax.set_ylabel('Frequency')
    ax.set_title('Character Frequency Distribution')

    # Display the plot using Streamlit
    st.pyplot(fig)

# Load 10,000 rows of data into the dataframe.
data = load_data(10000)

if data is not None:
    # Notify the reader that the data was successfully loaded.
    # Display abstract data
    display_abstract_data(data)
    # Display character frequency plot
    display_character_frequency_plot(data)
else:
    st.warning("Data loading failed. Please check the error message above.")
