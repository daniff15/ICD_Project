import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

st.title("Funding Analysis")

# Display the slider for selecting the number of countries to display
top_countries_count = st.slider("Select Number of Countries to Display", min_value=1, max_value=len(df["Country"].unique()), value=7)

# Display the bar chart for the number of publications by country
country_publications = df.groupby("Country")["Abstract"].count().reset_index()
country_publications.columns = ["Country", "Publications"]

# Sort the DataFrame based on the number of publications
country_publications = country_publications.sort_values(by="Publications", ascending=False)

# Select the top N countries based on the slider value
top_countries_df = country_publications.head(top_countries_count)

# Display information about funded publications
st.write("Funded and Not Funded Publications")

# Assuming "Funding Details" contains information about funding
df["Funded"] = df["Funding Details"].notnull()

avg_publications_by_country = df.groupby(["Country", "Funded"])["Title"].count().reset_index()
avg_publications_by_country.columns = ["Country", "Funded", "Number of Publications"]

# Filter the DataFrame based on the selected number of top countries
top_countries_avg_df = avg_publications_by_country[avg_publications_by_country["Country"].isin(top_countries_df["Country"])]

# Sort the DataFrame based on the total number of publications and the count of funded articles
top_countries_avg_df = top_countries_avg_df.sort_values(by=["Country", "Number of Publications", "Funded"],
                                                        ascending=[True, False, False])

# Create and display the bar chart
fig_avg_publications = px.bar(top_countries_avg_df, x="Number of Publications", y="Country", color="Funded",
                              orientation="h",
                              labels={"Country": "Country", "Funded": "Funding Status"},
                              color_discrete_map={"True": "green", "False": "red"})
st.plotly_chart(fig_avg_publications)

# Load the dataset
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

# Assuming "Funding Details" contains information about funding
df["Funded"] = df["Funding Details"].notnull()

# Convert 'Cited by' to numeric (assuming it contains numbers)
df['Cited by'] = pd.to_numeric(df['Cited by'], errors='coerce')

# Create and display the scatter plot
fig_scatter = px.scatter(df, x="Funded", y="Cited by", color="Funded",
                         title="Relationship Between Funding and Number of Citations",
                         labels={"Funded": "Funding Status", "Cited by": "Number of Citations"},
                         color_discrete_map={"True": "green", "False": "red"})
st.plotly_chart(fig_scatter)

# Create a pie chart using Altair
countries_count = df["Country"].value_counts(normalize=True).reset_index()
countries_count.columns = ["Country", "Percentage"]

# Display a table showing the number of citations and funding status for each article in the selected country
selected_country = st.selectbox("Select a Country", top_countries_df["Country"].unique())
if selected_country:
    # Filter the DataFrame for the selected country
    selected_country_df = df[df["Country"] == selected_country]
    
    # Sort the DataFrame by the number of citations
    citations_table = selected_country_df[["Title", "Cited by", "Funded"]].sort_values(by="Cited by", ascending=False)
    
    # Add a new column indicating whether the publication is funded or not
    citations_table["Funding Status"] = citations_table["Funded"].apply(lambda x: "Funded" if x else "Not Funded")
    
    # Display the sorted table
    st.table(citations_table[["Title", "Cited by", "Funding Status"]])
