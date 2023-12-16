import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

st.title("Publications by Country, Funding Relations, and Citations")

# Display the slider for selecting the number of countries to display
top_countries_count = st.slider("Select Number of Countries to Display", min_value=1, max_value=len(df["Country"].unique()), value=5)

# Display the bar chart for the number of publications by country
country_publications = df.groupby("Country")["Abstract"].count().reset_index()
country_publications.columns = ["Country", "Publications"]

# Sort the DataFrame based on the number of publications
country_publications = country_publications.sort_values(by="Publications", ascending=False)

# Select the top N countries based on the slider value
top_countries_df = country_publications.head(top_countries_count)

# Create and display the bar chart
fig_bar = px.bar(top_countries_df, x="Publications", y="Country", orientation="h",
                 title=f"Top {top_countries_count} Countries by Number of Publications",
                 labels={"Publications": "Number of Publications", "Country": "Country"})
st.plotly_chart(fig_bar)

# Display information about funded publications
st.subheader("Funding and Publications Relationship")

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

# Display information about funded publications
st.subheader("Funding and Citations Relationship")

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

# Create and display the pie chart
fig_pie = px.pie(countries_count, names="Country", values="Percentage", title="Percentage of Articles by Country")
fig_pie.update_traces(textposition='inside')
fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig_pie)

# Display a table showing the number of citations for each article in the selected country
selected_country = st.selectbox("Select a Country", top_countries_df["Country"].unique())
if selected_country:
    # Filter the DataFrame for the selected country
    selected_country_df = df[df["Country"] == selected_country]
    
    # Sort the DataFrame by the number of citations
    citations_table = selected_country_df[["Title", "Cited by"]].sort_values(by="Cited by", ascending=False)
    
    # Display the sorted table
    st.table(citations_table)
