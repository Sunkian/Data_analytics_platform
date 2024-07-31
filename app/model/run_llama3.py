import random
from TextGenerationInference import TGI, GenerateRequest, GenerateParameters
import json 
import re
import time 
from tqdm import tqdm as tqdm_bar
import streamlit as st

tgi_client = TGI(endpoint_name="huggingface-pytorch-tgi-inference-2024-07-31-08-41-02-341", region_name="us-east-1")

def batch_generate(model, params, prompts, batch_size):
    all_results = []
    for i in tqdm_bar(range(0, len(prompts), batch_size), desc="Generating"):
        batch_prompts = prompts[i: i + batch_size]
        requests = [GenerateRequest(inputs=prompt, parameters=params) for prompt in batch_prompts]
        batch_responses = model.create_from_objects(requests)
        all_results.extend(batch_responses)
    return all_results

# Title of the app
st.title('Natural Language to SQL with Llama 3 70B')

# Input for the query
query = st.text_input("Query")
st.write("Your query is: ", query)

# Input field for selecting the database format
db_format = st.selectbox("Select your database format:", 
                         ["MySQL", "PostgreSQL", "Snowflake", "SQLite", "Microsoft SQL Server"])

st.write("Selected Database Format:", db_format)

# Store the inputs in session state to reuse them later
if 'query' not in st.session_state:
    st.session_state.query = query
if 'db_format' not in st.session_state:
    st.session_state.db_format = db_format

# Improved prompt with placeholders
prompt_template = """
You are a helpful assistant specializing in data analysis in a {db_format} warehouse.
Answer the question by providing SQL code compatible with the {db_format} environment.
Question: {query}
"""

# Function to generate and display the response
def generate_and_display_response():
    # Replace placeholders with actual values
    prompt = prompt_template.format(db_format=st.session_state.db_format, query=st.session_state.query)

    params = GenerateParameters(max_new_tokens=1024, temperature=0.7)
    batch_size = 1
    batch_responses = batch_generate(tgi_client, params, [prompt], batch_size)

    # Print and return the response
    for response in batch_responses:
        st.write("Generated SQL Query:")
        st.code(response)

# Create a button to generate the SQL query
if st.button("Generate"):
    generate_and_display_response()