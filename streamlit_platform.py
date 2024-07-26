import streamlit as st

st.title('Natural Language to SQL with Llama 3 70B')

title = st.text_input("Query")
st.write("You query is: ", title)