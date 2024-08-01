# database.py
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
import yaml 
import json

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
    return None

# Load the config file
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

credentials_config = load_config('credentials.yaml')
database_info = load_json_file('platform_architecture.json')
# Database Configuration
user = credentials_config['credentials']['user']
password = credentials_config['credentials']['password']
host = credentials_config['credentials']['host']
database = credentials_config['credentials']['database']



# URL-encode the password
encoded_password = quote_plus(password)

# Construct the database URI
DATABASE_URI = f'mysql+pymysql://{user}:{encoded_password}@{host}/{database}'

# Function to connect to the MySQL database using SQLAlchemy
def connect_to_mysql():
    try:
        engine = create_engine(DATABASE_URI)
        return engine
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to execute SQL query and fetch results
def execute_sql_query(engine, query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()  # Get column names
            # Create a list of dictionaries where each dictionary represents a row
            results = [dict(zip(columns, row)) for row in result.fetchall()]
            return results
    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return None
    

# Function to get schema names, table names, and their columns
def get_database_architecture(engine):
    inspector = inspect(engine)
    architecture = {}
    try:
        schemas = inspector.get_schema_names()
        for schema in schemas:
            tables = inspector.get_table_names(schema=schema)
            schema_info = {}
            for table in tables:
                columns = inspector.get_columns(table, schema=schema)
                column_info = {col['name']: str(col['type']) for col in columns}
                schema_info[table] = column_info
            architecture[schema] = schema_info
    except SQLAlchemyError as e:
        st.error(f"Error fetching database architecture: {e}")
    return architecture
