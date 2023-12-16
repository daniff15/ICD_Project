import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# Assuming you have loaded your dataset into a DataFrame named df
# If not, load your dataset here
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

df['Funding'] = df['Funding Details'].notnull()

# Convert 'Cited by' to numeric (assuming it contains numbers)
df['Cited by'] = pd.to_numeric(df['Cited by'], errors='coerce')

# Plot the correlation using Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Funding', y='Cited by', data=df)
ax.set_title('Correlation Between Funding and Number of Citations')
ax.set_xlabel('Funding')
ax.set_ylabel('Number of Citations')

# Display the plot in Streamlit
st.pyplot(fig)
