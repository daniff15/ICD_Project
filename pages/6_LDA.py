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


# Baixar os recursos necessários para o NLTK
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Suprimir alguns avisos devido a versões antigas do pyLDAvis
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load the dataset
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

# Processamento de texto para LDA
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    # Remover caracteres especiais, números e converter para minúsculas
    text = re.sub(r'[^a-zA-Z]', ' ', str(text))
    text = text.lower()
    
    # Tokenização
    words = word_tokenize(text)
    
    # Remover stopwords e realizar stemming
    words = [ps.stem(word) for word in words if word not in stop_words and len(word) > 2]
    
    return words

# Aplicar pré-processamento aos resumos
df['Processed_Abstract'] = df['Abstract'].apply(preprocess_text)

# Remover documentos sem resumo após o pré-processamento
df = df[df['Processed_Abstract'].apply(len) > 0]

# Criar um dicionário e um corpus Gensim
dictionary = Dictionary(df['Processed_Abstract'])
corpus_gensim = [dictionary.doc2bow(text) for text in df['Processed_Abstract']]

# Treinar o modelo LDA
num_topics = 5  # Especifique o número desejado de tópicos
lda_model = LdaModel(corpus_gensim, num_topics=num_topics, id2word=dictionary)

# Criar a visualização do LDA
vis_data = gensimvis.prepare(lda_model, corpus_gensim, dictionary)

# Salvar a visualização como um arquivo HTML
pyLDAvis.save_html(vis_data, 'lda_visualization.html')

# Exibir o gráfico no Streamlit usando st.components
st.components.v1.html(open('lda_visualization.html', 'r', encoding='utf-8').read(), height=800, width=1200)


processed_texts = _preprocess_data(df)

# Create Dictionary
id2word = corpora.Dictionary(processed_texts)

coherence_model_lda = CoherenceModel(model=lda_model, texts=processed_texts, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
st.write('Coherence Score:', coherence_lda)