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

st.subheader("Types of documents")
# Read data from CSV file for document types
file_path_document_types = "./data/icd_scopus.csv"
df_document_types = pd.read_csv(file_path_document_types)

# Group by document type and count the occurrences
df_document_types_count = df_document_types.groupby("Document Type").size().reset_index(name="Count")

# Create a pie chart for document types
fig_document_types = px.pie(df_document_types_count, names="Document Type", values="Count",
                             title="Distribution of Publications by Document Type",
                             labels={"Count": "Number of Publications", "Document Type": "Document Type"})

# Display the chart for document types
st.plotly_chart(fig_document_types)


# Read data from CSV file for conference locations
file_path_conferences = "./data/icd_scopus.csv"
df_conferences = pd.read_csv(file_path_conferences)

# Drop NaN values in the "Conference location" column
df_conferences = df_conferences.dropna(subset=["Conference location"])

# Get the top N conference locations
top_locations = df_conferences["Conference location"].value_counts().nlargest(10).reset_index()
top_locations.columns = ["Conference location", "Count"]

# Create a bar chart for the top conference locations
fig_top_locations = px.bar(top_locations, x="Conference location", y="Count",
                            title="Conference Locations",
                            labels={"Count": "Number of Conferences", "Conference location": "Location"})

# Display the chart for the top conference locations
st.plotly_chart(fig_top_locations)

