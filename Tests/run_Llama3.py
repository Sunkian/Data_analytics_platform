from TextGenerationInference import TGI, GenerateRequest, GenerateParameters
import requests

# Initialize TGI client
tgi_client = TGI(endpoint_name="huggingface-pytorch-tgi-inference-2024-08-01-16-41-32-607", region_name="us-east-1")

# Function to generate SQL from the prompt
def generate_sql(tgi, type, query, schema):
    #prompt = f"Please translate the following query into SQL code: \n\n #Given query:# {query}\n\n #SQL code# \n\n"
    prompt = f"""
        You are a helpful assistant specializing in data analysis in a {type} database. \n\n
        Answer the question by providing SQL code compatible with the {type} environment. \n\n
        Question: \n\n 
        {query}
        \n\n 
        ### Database Schema \n
        This query will run on a database whose schema is represented as follows: \n\n 
        {schema}
        \n\n 
        ### SQL \n
        Given the database schema, here is the SQL query that answers the question:\n\n
        
        """


    params = GenerateParameters(max_new_tokens=512, temperature=0.2, stop=["#SQL code#", "\n\n", "\"\"\""])
    request = GenerateRequest(inputs=prompt, parameters=params)
        
    response = tgi.create_from_objects([request])[0]
    return response

# Function to extract SQL code from response
def extract_sql(response):
    marker = "answers the question:"
    marker_index = response.find(marker)
    if marker_index != -1:
        # Extract everything after the marker, keeping all formatting
        sql_code = response[marker_index + len(marker):]
        return sql_code
    return None


# Function to send SQL code to Flask API
def send_to_flask_api(sql_code):
    api_url = "http://127.0.0.1:5000/receive-sql"  # Replace with your Flask API URL
    payload = {"sql_code": sql_code}
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send SQL code to Flask API. Error: {e}")
        return None



# ===== Test =====

def generate_sql_test(tgi):
    #prompt = f"Please translate the following query into SQL code: \n\n #Given query:# {query}\n\n #SQL code# \n\n"
    prompt = f"""
        You are a helpful assistant specializing in data analysis in a MySQL database. \n\n
        Answer the question by providing SQL code compatible with the MySQL environment. \n\n
        Question: \n\n 
        Give me the number of laptops that Aaron placed.
        \n\n 
        ### Database Schema \n
        This query will run on a database whose schema is represented as follows: \n\n 
        {{
            "platform": {{
                "orders": {{
                    "orderID": "INTEGER",
                    "userName": "VARCHAR(50)",
                    "orderType": "VARCHAR(255)",
                    "purchaseDate": "DATE"
                }},
                "products": {{
                    "productID": "INTEGER",
                    "productType": "VARCHAR(50)",
                    "operatingSystem": "VARCHAR(50)"
                }}
            }}
        }}
        \n\n 
        ### SQL \n
        Given the database schema, here is the SQL query that answers the question:\n\n
        
        """

    params = GenerateParameters(max_new_tokens=512, temperature=0.2, stop=["#SQL code#", "\n\n", "\"\"\""])
    request = GenerateRequest(inputs=prompt, parameters=params)
        
    response = tgi.create_from_objects([request])[0]
    return response


""" # Generate SQL code using LLM
response = generate_sql_test(tgi_client)
print("Full response:", response)

# Extract SQL code
sql_code = extract_sql(response)
if sql_code:
    print("Extracted SQL code:", sql_code)
    # Send extracted SQL code to Flask API
    send_to_flask_api(sql_code)
else:
    print("No SQL code found in the response.") """



""" # Load the database schema from JSON file
def load_schema():
    try:
        with open("platform_architecture.json", "r") as f:
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
#You are a helpful assistant specializing in data analysis in a {db_format} warehouse.
#Answer the question by providing SQL code compatible with the {db_format} environment.
#Question: {query}

### Database Schema
#This query will run on a database whose schema is represented as follows:
##{schema}

### SQL
#Given the database schema, here is the SQL query that answers the question:
#```sql
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
 """