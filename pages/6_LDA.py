from multiprocessing import freeze_support
from matplotlib import _preprocess_data
import pandas as pd
import pyLDAvis
import streamlit as st
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import pyLDAvis.gensim_models as gensimvis
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from gensim.models.coherencemodel import CoherenceModel
import gensim.corpora as corpora
from nbimporter import NotebookLoader
from main2 import lda_unique_country, unique_countries

# Ensure the code inside this block is only executed when the script is run directly
if __name__ == '__main__':
    # The following line is not necessary if your program is not going to be frozen
    freeze_support()

    # Get the list of unique countries
    unique_country = unique_countries()

    # Create a Streamlit app
    st.title("LDA Visualization for Unique Countries")

    # Allow the user to select a country from the unique_country list
    selected_country = st.selectbox("Select a country", unique_country)

    # Run LDA and get visualization for the selected country
    vis = lda_unique_country(selected_country)

    # Save the visualization as an HTML file
    pyLDAvis.save_html(vis, 'lda_visualization.html')

    # Display the HTML file in the Streamlit app
    st.components.v1.html(open('lda_visualization.html', 'r', encoding='utf-8').read(), height=800, width=1200)
