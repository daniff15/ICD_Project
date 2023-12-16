import streamlit as st
import pandas as pd
import re
import altair as alt

with open("styles.css", "r") as f:
    custom_css = f.read()

# Inject custom CSS
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# Read data from CSV file
file_path = "./data/icd_scopus.csv"
df = pd.read_csv(file_path)

# Drop rows where there are no authors
df = df.dropna(subset=["Author full names"])

df["Author full names"] = df["Author full names"].fillna("")

# Extract unique authors and their order of appearance
authors_with_order = [re.sub(r'\s*\(\d+\)', '', author.strip()) for line in df["Author full names"] for author in line.split(';')]
unique_authors = list(dict.fromkeys(authors_with_order))

st.title("Publications by Author")

top_authors = pd.Series(authors_with_order).value_counts().head(10)

# Order unique_authors by number of articles
unique_authors = pd.Series(authors_with_order).value_counts().index.tolist()    

# Sidebar with author selection (allowing only one selection)
selected_author = st.sidebar.selectbox("Select an Author", unique_authors)

if not selected_author:
    st.warning("Please select an author.")
else:
    filtered_df = df[df["Author full names"].apply(lambda x: selected_author.lower() in x.lower())]

    if filtered_df.empty:
        st.info(f"No articles found where the selected author co-authored: {selected_author}")
    else:
        # Display phrases above each table with a 3:1 column display
        col1, col2 = st.columns([3, 1])  # Adjust the proportions here
        with col1:
            st.write(f"Publications for {selected_author}:")
            st.table(filtered_df[["Title", "Author full names"]])

        with col2:
            st.write("Top 10 Authors with Most Articles:")
            st.table(top_authors.reset_index().rename(columns={"index": "Author", 0: "Number of Articles"}))

        # Create a dictionary to store the number of citations for each author
        author_citations = {}

        # Iterate through each article
        for index, row in df.iterrows():
            # Split authors by ';'
            authors = [re.sub(r'\s*\(\d+\)', '', author.strip()) for author in row["Author full names"].split(';')]
            
            # Update the dictionary with the number of citations for each author
            for author in authors:
                if author in author_citations:
                    author_citations[author] += row["Cited by"]
                else:
                    author_citations[author] = row["Cited by"]

        # Display the top 10 authors in a bar chart
        top_cited_authors_df = pd.DataFrame(list(author_citations.items()), columns=["Author", "Total Citations"])
        top_cited_authors_df = top_cited_authors_df.sort_values(by="Total Citations", ascending=False).head(10)

        # Add a bar chart displaying the most cited authors
        st.write(f"Top 10 Authors by Total Citations")

        # Add the selected author to the top cited authors
        if selected_author not in top_cited_authors_df["Author"].tolist():
            # Add the selected author with their total citations (if available)
            if selected_author in author_citations:
                selected_author_citations = author_citations[selected_author]
            else:
                selected_author_citations = 0

            # Create a list of dictionaries for the selected author
            selected_author_data = [{"Author": selected_author, "Total Citations": selected_author_citations}]

            # Convert the list to a DataFrame and concatenate it with top_cited_authors_df
            top_cited_authors_df = pd.concat([top_cited_authors_df, pd.DataFrame(selected_author_data)], ignore_index=True)

        # Sort the dataframe again after adding the selected author

        if selected_author not in top_cited_authors_df["Author"].tolist():
            top_cited_authors_df = top_cited_authors_df.sort_values(by="Total Citations", ascending=False).head(10)
        else:
            top_cited_authors_df = top_cited_authors_df.sort_values(by="Author", ascending=True)

        # Add a bar chart displaying the most cited authors
        chart = alt.Chart(top_cited_authors_df).mark_bar().encode(
            x=alt.X("Total Citations:Q", title="Total Citations"),
            y=alt.Y("Author:N", title="Author", sort="-x"),
            opacity=alt.condition(
                alt.datum.Author == selected_author,
                alt.value(1),
                alt.value(0.4)
            )
        ).properties(width=600, height=400)

        st.altair_chart(chart, use_container_width=True)
