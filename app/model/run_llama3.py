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
st.write("Your query is:", query)

# Input field for selecting the database format
db_format = st.selectbox("Select your database format:", 
                         ["MySQL", "PostgreSQL", "Snowflake", "SQLite", "Microsoft SQL Server"])

st.write("Selected Database Format:", db_format)

# Load the database schema from JSON file
def load_schema():
    try:
        with open("selected_database_architecture.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Database schema file not found.")
        return None

# Convert schema dictionary to a string
def schema_to_string(schema_dict):
    schema_str = ""
    for schema, tables in schema_dict.items():
        schema_str += f"Schema: {schema}\n"
        for table, columns in tables.items():
            schema_str += f"Table: {table} (\n"
            for col_name, col_type in columns.items():
                schema_str += f"  {col_name} {col_type},\n"
            schema_str = schema_str.rstrip(",\n") + "\n)\n\n"
    return schema_str

# Improved prompt with placeholders
prompt_template = """
You are a helpful assistant specializing in data analysis in a {db_format} warehouse.
Answer the question by providing SQL code compatible with the {db_format} environment.
Question: {query}

### Database Schema
This query will run on a database whose schema is represented as follows:
{schema}

### SQL
Given the database schema, here is the SQL query that answers the question:
```sql
"""

# Function to generate and display the response
def generate_and_display_response():
    schema_dict = load_schema()
    if schema_dict is None:
        return
    schema_str = schema_to_string(schema_dict)

    # Replace placeholders with actual values
    prompt = prompt_template.format(
        db_format=st.session_state.db_format, 
        query=st.session_state.query,
        schema=schema_str
    )

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
