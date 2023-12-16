import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file
file_path = "./data/Scopus-10-Analyze-Year.csv"
df = pd.read_csv(file_path)

st.title("Yearly Publications Plot")

# Sidebar with year selection
selected_year = st.sidebar.slider("Select Year", min_value=int(df["YEAR"].min()), max_value=int(df["YEAR"].max()))

# Filter data based on selected year and all previous years
filtered_df = df[df["YEAR"] <= selected_year]

st.write("Data till selected year: ", selected_year)

fig, ax = plt.subplots()
ax.plot(filtered_df["YEAR"], filtered_df["PUBLICATIONS"], marker='o', label='Publications', linestyle='-', color='b')
ax.set_title(f"Publications Over Years (Up to {selected_year})")
ax.set_xlabel("Year")
ax.set_ylabel("Publications")
ax.legend()

# Add text annotation for the total publications for each year
for i, value in enumerate(filtered_df["PUBLICATIONS"]):
    ax.text(filtered_df["YEAR"].iloc[i], value, str(value), ha='center', va='bottom')

total_publications = filtered_df["PUBLICATIONS"].sum()
st.write(f"Total Publications So Far: {total_publications}")

st.pyplot(fig)

# Additional Information
st.subheader("Additional Information:")
st.write(f"Average Publications per Year: {filtered_df['PUBLICATIONS'].mean():.2f}")
