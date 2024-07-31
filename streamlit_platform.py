import streamlit as st
import json

st.title('Natural Language to SQL with Llama 3 70B')

# Input field for natural language query
query = st.text_input("Enter your query:")
st.write("Your query is:", query)

# Input field for selecting the database format
db_format = st.selectbox("Select your database format:", 
                         ["MySQL", "PostgreSQL", "Snowflake", "SQLite", "Microsoft SQL Server"])

st.write("Selected Database Format:", db_format)

# Store the inputs in session state to reuse them later
if 'query' not in st.session_state:
    st.session_state.query = query
if 'db_format' not in st.session_state:
    st.session_state.database_format = db_format