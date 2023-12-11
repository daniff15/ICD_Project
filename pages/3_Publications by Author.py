import streamlit as st
import pandas as pd
import re

# Read data from CSV file
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

df["Author full names"] = df["Author full names"].fillna("")

# Create a list of unique authors without AuthorID
all_authors = [re.sub(r'\s*\(\d+\)', '', author.strip()) for line in df["Author full names"] for author in line.split(';')]
unique_authors = list(set(all_authors))

st.title("Publications by Author")

# Sidebar with author selection (allowing multiple selection)
selected_authors = st.sidebar.multiselect("Select Authors", unique_authors)

filtered_df = df[df["Author full names"].apply(lambda x: all(author.lower() in x.lower() for author in selected_authors))]

if not selected_authors:
    st.warning("Please select one or more authors.")
elif filtered_df.empty:
    st.info(f"No articles found where the selected authors co-authored: {'; '.join(selected_authors)}")
else:
    st.write(f"Publications for {'; '.join(selected_authors)}:")
    st.table(filtered_df[["Title", "Author full names"]])
