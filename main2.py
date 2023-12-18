# %% [markdown]
# # ICD Project

# %% [markdown]
# ## Importing libraries

# %%
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import CountVectorizer
import contractions
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk import pos_tag
import gensim
import gensim.corpora as corpora
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.corpora import Dictionary
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from gensim.models.ldamodel import LdaModel
from gensim.models import CoherenceModel

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# %% [markdown]
# ## Load Dataset

# %%
data = pd.read_csv('./data/icd_scopus.csv')

# %% [markdown]
# ## Basic exploratory content analysis

# %% [markdown]
# ### Understanding the dataset

# %%
# Checking the shape of the dataset

# %%
# View the first 5 rows of the dataset

# %% [markdown]
# ## Data Cleaning

# %% [markdown]
# ### Checking for duplicate rows

# %%

# %% [markdown]
# ### Cheking for null values
# 

# %%
# Checking for missing values





# %%
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Combine all text columns into a single series
text_series = data.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# Tokenize the text
all_text = ' '.join(text_series)
tokens = word_tokenize(all_text)
tokens = [word.lower() for word in tokens if word.isalpha()]

# Count word occurrences
word_counts = Counter(tokens)

# Display the most common words
most_common_words = word_counts.most_common(10)  # Change 10 to the desired number of most common words





# %% [markdown]
# ## Basic Text pre-processing

# %% [markdown]
# ### Remove useless columns in the context and columns with NaN values

# %%
columns_to_drop = ['Author(s) ID', 'Author full names', 'Volume', 'Issue', 'Art. No.', 'Funding Details', 'Conference code', 'Conference location', 'Conference name', 'Conference date', 'Funding Texts', 'Editors', 'Open Access', 'Page start', 'Page end', 'Page count', 'Cited by', 'DOI', 'Link', 'Affiliations', 'Authors with affiliations', 'Sponsors', 'Molecular Sequence Numbers', 'Chemicals/CAS', 'Tradenames', 'Manufacturers', 'ISBN', 'CODEN', 'PubMed ID', 'Authors', 'Year', 'Index Keywords', 'References', 'Correspondence Address', 'Publisher', 'ISSN', 'Language of Original Document', 'Document Type', 'Publication Stage', 'Source', 'EID']

droped_data = data.drop(columns=columns_to_drop)

# %%
# Get the number of duplicates
duplicate = droped_data['Abstract'].duplicated().sum()

# Remove duplicate rows
droped_data = droped_data.drop_duplicates(subset=['Abstract'])

# %%

#do the same for title
# Get the number of duplicates
duplicate = droped_data['Title'].duplicated().sum()

# Remove duplicate rows
droped_data = droped_data.drop_duplicates(subset=['Title'])

# %%
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Combine all text columns into a single series
text_series = droped_data.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# Tokenize the text
all_text = ' '.join(text_series)
tokens = word_tokenize(all_text)

# Remove stopwords and punctuation
stop_words = set(stopwords.words('english'))
custom_words = set(['pp', 'de'])
stop_words.update(custom_words)
tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words and word not in string.punctuation]

# Count word occurrences
word_counts = Counter(tokens)

# Display the most common words
most_common_words = word_counts.most_common(10)  # Change 10 to the desired number of most common words





# %% [markdown]
# ## **2. Preprocess the dataset**
# 

# %% [markdown]
# ### Clean up function

# %%
def clean_text(text_string, punctuations=r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''):
    # Cleaning the urls
    string = re.sub(r'https?://\S+|www\.\S+', '', text_string)

    # Cleaning the html elements
    string = re.sub(r'<.*?>', '', string)

    # Removing the punctuations
    string = re.sub(r'[^\w\s]', '', string)

    # Converting the text to lower
    string = string.lower()

    # Removing stop words
    filtered_words = [word for word in string.split() if word not in stopwords.words('english')]

    # Custom stop words list
    customlist = ['not', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
                  "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
                  "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
                  "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    # Applying custom stop words
    final_words = list(set(filtered_words) - set(customlist))

    # Tokenization
    tokens = word_tokenize(' '.join(final_words))

    # Remove numbers
    tokens = [word for word in tokens if word.isalpha()]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in lemmatized_words]

    # Fix contractions
    final_string = ' '.join([contractions.fix(word) for word in stemmed_words])

    return final_string

# %%

# %%
#converts all the values in a specific columns of the DataFrame data to strings 
droped_data["Abstract"] = droped_data["Abstract"].astype(str) 

#Applying a Text Cleaning Function
droped_data['clean_Abstract'] = droped_data['Abstract'].apply(clean_text)

# %%

# %%
#... aims to create a new DataFrame called selected_columns that contains only the "Title" and "cleanTitle" columns from the original DataFrame df. Then, it displays the first 20 rows of this new DataFrame using the .head(20) method.
selected_columns = droped_data[['Abstract', 'clean_Abstract']]



# %% [markdown]
# ## Advanced text processing

# %% [markdown]
# ### Bag-Of-Words ou 1 gram

# %%
# Initialize CountVectorizer
vectorizer = CountVectorizer()

# Fit and transform the 'cleanTitle' column
X = vectorizer.fit_transform(droped_data['clean_Abstract'])

# Convert the BoW array into a DataFrame
bow_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Show the resulting DataFrame



# %% [markdown]
# ### Term Frequency-Inverse Document Frequency (TF-IDF)

# %%
# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the cleaned abstracts
tfidf_matrix = tfidf_vectorizer.fit_transform(droped_data['clean_Abstract'])

# Convert to array and then to DataFrame for better visualization
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())




# %% [markdown]
# *Bar Plot for Most Common TF-IDF*
# 
# You can use a bar plot to visualize the most common TF-IDF in the corpus.




# %% [markdown]
# ## Part of Speech (POS) Tagging

# %%
# Function to tag POS in a sentence
def pos_tag_sentence(sentence):
    tokens = word_tokenize(sentence)
    return pos_tag(tokens)

# Apply POS tagging to each cleaned abstract
droped_data['POS_Tagged_Abstract'] = droped_data['clean_Abstract'].apply(pos_tag_sentence)




# %% [markdown]
# **Frequency Distribution of POS Tags**
# 
# Bar chart to show the frequency distribution of different POS tags across all abstracts.






# %% [markdown]
# **Pie Chart for Overall Tag Distribution**




# %%
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

def unique_countries():
    # Assuming droped_data is your DataFrame and 'clean_Abstract' is the column with abstracts
    unique_countries = droped_data['Country'].unique()
    return unique_countries

# Function to preprocess data for a specific country
def preprocess_data_for_country(df, country):
    documents = df[df['Country'] == country]['clean_Abstract']
    texts = [[word for word in simple_preprocess(str(doc))] for doc in documents]
    return texts

# Iterate through each unique country and perform topic modeling
country = 'Portugal'

def lda_unique_country(country):

    # Preprocess data for the current country
    processed_texts = preprocess_data_for_country(droped_data, country)

    print(f"Number of documents for {country}: {len(processed_texts)}")

    if not processed_texts:
        print(f"No documents for {country}. Skipping.")
        
    else:

        # Create Dictionary
        id2word = corpora.Dictionary(processed_texts)

        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in processed_texts]

        # Set number of topics
        num_topics = 10
        lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics, alpha='auto', per_word_topics=True)

        

        # Coherence Score
        coherence_model_lda = CoherenceModel(model=lda_model, texts=processed_texts, dictionary=id2word, coherence='c_v')
        #coherence_lda = coherence_model_lda.get_coherence()
        

        vis = gensimvis.prepare(lda_model, corpus, id2word)

        return vis
    





