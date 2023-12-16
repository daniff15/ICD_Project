import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

st.title("Yearly Publications Plot")

# Sidebar with year selection
selected_year = st.sidebar.slider("Select Year", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()))

# Filter data based on selected year and all previous years
filtered_df = df[df["Year"] <= selected_year]

st.write("Data till selected year: ", selected_year)

# Create dictionary to store the number of publications for each year
year_publications = {}

# Iterate through each article
for index, row in df.iterrows():
    # Update the dictionary with the number of publications for each year
    if row["Year"] in year_publications:
        year_publications[row["Year"]] += 1
    else:
        year_publications[row["Year"]] = 1

# Create a DataFrame from the dictionary
year_publications_df = pd.DataFrame.from_dict(year_publications, orient='index', columns=["Publications"])

# Sort the DataFrame by the index (year)
year_publications_df = year_publications_df.sort_index()

# Create a line plot with annotations
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(year_publications_df.index, year_publications_df["Publications"], marker='o', linestyle='-')
ax1.set(xlabel="Year", ylabel="Number of Publications", title="Number of Publications by Year")
ax1.set_xticks(year_publications_df.index)
ax1.set_xticklabels(year_publications_df.index, rotation=90)
ax1.grid()

# Annotate each data point
for index, value in enumerate(year_publications_df["Publications"]):
    ax1.text(year_publications_df.index[index], value, str(value), ha='center', va='bottom')

# Display the first plot
st.pyplot(fig1)

# Create a bar chart for top countries using a separate Axes object
fig2, ax2 = plt.subplots(figsize=(10, 4))
top_countries = df[df['Year'] <= selected_year]['Country'].value_counts().head(10)
ax2.bar(top_countries.index, top_countries.values, color='skyblue')
ax2.set(xlabel="Country", ylabel="Number of Publications", title=f"Top 10 Countries in {selected_year}")
ax2.tick_params(axis='x', rotation=45)
ax2.grid()

# Display the second plot
st.pyplot(fig2)
