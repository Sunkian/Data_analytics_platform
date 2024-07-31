import random
from TextGenerationInference import TGI, GenerateRequest, GenerateParameters
import json 
import re
import time 
from tqdm import tqdm as tqdm_bar
from streamlit_platform import

tgi_client = TGI(endpoint_name="huggingface-pytorch-tgi-inference-2024-07-31-08-41-02-341", region_name="us-east-1")

def batch_generate(model, params, prompts, batch_size):
    all_results = []
    for i in tqdm_bar(range(0, len(prompts), batch_size), desc="Generating"):
        batch_prompts = prompts[i: i + batch_size]
        requests = [GenerateRequest(inputs=prompt, parameters=params) for prompt in batch_prompts]
        batch_responses = model.create_from_objects(requests)
        all_results.extend(batch_responses)
    return all_results

# Improved prompt
prompt = """
You are a helpful assistant specialising in data analysis in a snowflake warehouse.
Answer the questions by providing SQL code that is compatible with the snowflake environment.
This is the question you are required to answer: 
What is the total number of customers in the Chocolate Haven branch?

Here is the relevant context of the database:
create or replace TABLE CUSTOMER_DETAILS (
    CUSTOMER_ID NUMBER(38,0) NOT NULL,
    FIRST_NAME VARCHAR(255),
    LAST_NAME VARCHAR(255),
    EMAIL VARCHAR(255),
    PHONE VARCHAR(20),
    ADDRESS VARCHAR(255),
    primary key (CUSTOMER_ID)
);
"""
params = GenerateParameters(max_new_tokens=1024, temperature=0.7)
batch_size = 1
batch_responses = batch_generate(tgi_client, params, [prompt], batch_size)

# Print and return the response
for response in batch_responses:
    print(response)

# Return the response
batch_responses
