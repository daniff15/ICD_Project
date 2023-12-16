import pandas as pd
import plotly.express as px
import streamlit as st

# Read data from CSV file
file_path_subjects = "./data/Scopus-384-Analyze-Subject.csv"
df_subjects = pd.read_csv(file_path_subjects)

# Display the data
st.title("Publications by Subject Area")

# Create a bar chart
fig_subjects = px.bar(df_subjects, x="PUBLICATIONS", y="SUBJECT AREA",
                      orientation="h",
                      title="Number of Publications in Different Subject Areas",
                      labels={"PUBLICATIONS": "Number of Publications", "SUBJECT AREA": "Subject Area"})

# Display the chart
st.plotly_chart(fig_subjects)
