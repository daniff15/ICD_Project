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

# Especifique o caminho do arquivo Jupyter Notebook (substitua 'notebook.ipynb' pelo caminho do seu arquivo)
loader = NotebookLoader()
main = loader.load_module("./main.ipynb")

vis = main.lda_unique_country("Portugal")

# Salvar a visualização como um arquivo HTML
pyLDAvis.save_html(vis, 'lda_visualization.html')

# Exibir o gráfico no Streamlit usando st.components
st.components.v1.html(open('lda_visualization.html', 'r', encoding='utf-8').read(), height=800, width=1200)