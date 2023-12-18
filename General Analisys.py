import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import re

# Download NLTK stopwords (run this line once)
import nltk
nltk.download('stopwords')

# Display the data for the bar chart
st.title("Gamification enhances student participation?")
st.markdown("Gamification is the use of game design elements in non-game contexts. "
            "In education, gamification is used to increase student participation and engagement by incorporating game elements in learning environments. "
            "Gamification is an area that is being more and more applied to different areas.")

# Preprocess the text data
def preprocess_text(text):
    # Convert to lowercase if it's a string
    if isinstance(text, str):
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        text = ' '.join([word for word in text.split() if word not in stop_words])
    else:
        # Convert float values to empty strings
        text = ""
    return text

# Read data from CSV file for the word cloud
file_path_subjects_wordcloud = "./data/icd_scopus.csv"
df_subjects_wordcloud = pd.read_csv(file_path_subjects_wordcloud)

# Generate global word cloud
st.subheader("Global Word Cloud")

# Preprocess the text data for the entire dataset
df_subjects_wordcloud["Index Keywords"] = df_subjects_wordcloud["Index Keywords"].apply(preprocess_text)

# Generate global word cloud
wordcloud_global = WordCloud(width=800, height=400, background_color="white").generate(" ".join(df_subjects_wordcloud["Index Keywords"]))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_global, interpolation="bilinear")
plt.axis("off")
plt.title("Global Word Cloud of Keywords")
st.pyplot(plt)

# Handle NaN values and convert to strings
df_subjects_wordcloud["Index Keywords"] = df_subjects_wordcloud["Index Keywords"].fillna("").astype(str)

# Allow user to select a country
selected_country = st.selectbox("Select a Country", df_subjects_wordcloud["Country"].unique(), index=df_subjects_wordcloud["Country"].unique().tolist().index("Spain"))

# Generate word cloud for the selected country with text preprocessing
st.subheader(f"Word Cloud for {selected_country}")

# Filter data for the selected country
selected_country_data = df_subjects_wordcloud[df_subjects_wordcloud["Country"] == selected_country]

# Apply preprocessing to the "Index Keywords" column
selected_country_data["Index Keywords"] = selected_country_data["Index Keywords"].apply(preprocess_text)

# Generate word cloud for the selected country
wordcloud_country = WordCloud(width=800, height=400, background_color="white").generate(" ".join(selected_country_data["Index Keywords"]))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_country, interpolation="bilinear")
plt.axis("off")
plt.title(f"Word Cloud of Keywords for {selected_country}")
st.pyplot(plt)

# Read data from CSV file for the bar chart
file_path_subjects_bar = "./data/Scopus-384-Analyze-Subject.csv"
df_subjects_bar = pd.read_csv(file_path_subjects_bar)

st.subheader("Gamification in different subject areas")
# Create a bar chart for subject areas
fig_subjects_bar = px.bar(df_subjects_bar, x="PUBLICATIONS", y="SUBJECT AREA",
                          orientation="h",
                          title="Number of Publications in Different Subject Areas",
                          labels={"PUBLICATIONS": "Number of Publications", "SUBJECT AREA": "Subject Area"})

# Display the chart for subject areas
st.plotly_chart(fig_subjects_bar)
