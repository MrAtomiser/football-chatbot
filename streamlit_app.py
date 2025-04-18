import streamlit as st
import pandas as pd

# Load data (use cached version in real app)
df = pd.read_excel("opportunities.xlsx", sheet_name=" Opportunities for ballers main")
df.columns = [col.strip() for col in df.columns]
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Search function
def search_opportunities(query, df):
    query = query.lower()
    results = df[
        df.apply(lambda row: query in str(row['Type']).lower()
                              or query in str(row['Organizer']).lower()
                              or query in str(row['Country']).lower()
                              or query in str(row['City']).lower()
                              or query in str(row['Instagram Handles']).lower(), axis=1)
    ]
    return results[['Type', 'Organizer', 'Date', 'Country', 'City', 'Instagram link to the opportunity']].head(10)

# Streamlit UI
st.title("Football Opportunity Finder 🇳🇬⚽")
st.write("Ask me about trials, camps, or scouting events across Africa!")

query = st.text_input("What are you looking for?")

if query:
    results = search_opportunities(query, df)
    if not results.empty:
        st.write("### Results:")
        for _, row in results.iterrows():
            st.markdown(f"**{row['Type']}** - {row['Organizer']}  ")
            st.markdown(f"📍 {row['City']}, {row['Country']} | 📅 {row['Date'].date()}  ")
            st.markdown(f"🔗 [Instagram Link]({row['Instagram link to the opportunity']})")
            st.markdown("---")
    else:
        st.write("No matching opportunities found. Try another keyword!")
