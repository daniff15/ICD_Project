import streamlit as st
import pandas as pd
import plotly.express as px

# Read data from CSV file
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

# Handle NaN values in the "Affiliations" column
df["Affiliations"] = df["Affiliations"].fillna("")

# Create a list of unique affiliations
all_affiliations = [affiliation.strip() for line in df["Affiliations"] for affiliation in line.split(';')]
unique_affiliations = list(set(all_affiliations))

st.title("Publications by Affiliation")

# Option to select multiple affiliations
selected_affiliations = st.multiselect(
    "Select Affiliations",
    options=unique_affiliations,
    default=[affiliation for affiliation in unique_affiliations if affiliation != ""][:5]
)

filtered_df = df[df["Affiliations"].apply(lambda x: any(affiliation.lower() in x.lower() for affiliation in selected_affiliations))]

total_articles = len(filtered_df)

if total_articles == 0:
    st.warning("No publications found for the selected affiliations.")
else:
    affiliation_counts = filtered_df.groupby("Affiliations").size().reset_index(name="Publication Count")
    affiliation_counts = affiliation_counts.sort_values(by="Publication Count", ascending=False)  # Order by most publications
    affiliation_counts = affiliation_counts.head(10)  # Select top 10
    fig = px.bar(affiliation_counts, y="Publication Count", x="Affiliations", title="Affiliation Publication Counts")
    st.plotly_chart(fig)
