import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# Load data
df = pd.read_excel("opportunities .xlsx")
df.columns = [col.strip() for col in df.columns]
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# GPT-powered filter extraction
def extract_filters(query, openai_key):
    openai.api_key = openai_key
    prompt = f"""Extract relevant filters from the following football opportunity query.
Return a Python dictionary with keys: country, city, month, type, free (True/False).
Query: "{query}" """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        filters = eval(response['choices'][0]['message']['content'])
        return filters
    except Exception as e:
        st.error(f"Error from OpenAI: {e}")
        return None

# Apply filters to DataFrame
def filter_opportunities(filters, df):
    filtered = df.copy()
    if filters.get('country'):
        filtered = filtered[filtered['Country'].str.contains(filters['country'], case=False, na=False)]
    if filters.get('city'):
        filtered = filtered[filtered['City'].str.contains(filters['city'], case=False, na=False)]
    if filters.get('month'):
        try:
            month_num = datetime.strptime(filters['month'], '%B').month
            filtered = filtered[filtered['Date'].dt.month == month_num]
        except:
            pass
    if filters.get('type'):
        filtered = filtered[filtered['Type'].str.contains(filters['type'], case=False, na=False)]
    if filters.get('free') is True:
        filtered = filtered[filtered['Fee'].fillna('').str.contains('free|none|0', case=False)]
    return filtered[['Type', 'Organizer', 'Date', 'Country', 'City', 'Instagram link to the opportunity']].head(10)

# Streamlit app UI
st.title("Football Opportunity Finder 🇳🇬⚽ + GPT")
st.write("Ask about trials, camps, or scouting events across Africa!")

openai_key = st.text_input("Enter your OpenAI API key", type="password")

if openai_key:
    query = st.text_input("What are you looking for?")

    if query:
        filters = extract_filters(query, openai_key)
        if filters:
            st.write("### GPT extracted filters:")
            st.json(filters)
            results = filter_opportunities(filters, df)
            if not results.empty:
                st.write("### Results:")
                for _, row in results.iterrows():
                    st.markdown(f"**{row['Type']}** - {row['Organizer']}")
                    st.markdown(f"📍 {row['City']}, {row['Country']} | 📅 {row['Date'].date()}")
                    st.markdown(f"🔗 [Instagram Link]({row['Instagram link to the opportunity']})")
                    st.markdown("---")
            else:
                st.warning("No matching opportunities found.")
