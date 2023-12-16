import streamlit as st
import pandas as pd
import plotly.express as px

with open("styles.css", "r") as f:
    custom_css = f.read()

# Inject custom CSS
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# Read data from CSV file
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

# Handle NaN values in the "Affiliations" column
df["Affiliations"] = df["Affiliations"].fillna("")

# Create a list of unique affiliations
all_affiliations = [affiliation.strip() for line in df["Affiliations"] for affiliation in line.split(';')]
unique_affiliations = list(set(all_affiliations))

st.title("Publications by Affiliation")

# Calculate publication counts for each affiliation
affiliation_counts = df.groupby("Affiliations").size().reset_index(name="Publication Count")
affiliation_counts = affiliation_counts.sort_values(by="Publication Count", ascending=False)

# Select top 5 affiliations with the highest publication counts, excluding empty string
default_affiliations = list(affiliation_counts[affiliation_counts["Affiliations"] != ""].head(5)["Affiliations"])

# Option to select multiple affiliations
selected_affiliations = st.multiselect(
    "Select Affiliations",
    options=unique_affiliations,
    default=default_affiliations
)

filtered_df = df[df["Affiliations"].apply(lambda x: any(affiliation.lower() in x.lower() for affiliation in selected_affiliations))]

total_articles = len(filtered_df)

if total_articles == 0:
    st.warning("No publications found for the selected affiliations.")
else:
    affiliation_counts = filtered_df.groupby("Affiliations").size().reset_index(name="Publication Count")
    affiliation_counts = affiliation_counts.sort_values(by="Publication Count", ascending=False)
    affiliation_counts = affiliation_counts.head(10)
    fig = px.bar(affiliation_counts, y="Publication Count", x="Affiliations", title="Affiliation Publication Counts",
                 labels={"Affiliations": "Affiliation", "Publication Count": "Number of Publications"})
    st.plotly_chart(fig)
