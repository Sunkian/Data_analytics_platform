import streamlit as st
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
import json

# Database Configuration
user = 'root'
password = '@Freestyle678'  # Password with special characters
host = 'localhost'
database = 'platform'

# URL-encode the password
encoded_password = quote_plus(password)

# Construct the database URI
DATABASE_URI = f'mysql+pymysql://{user}:{encoded_password}@{host}/{database}'

# Initialize the database connection
@st.cache_resource
def init_connection():
    try:
        engine = create_engine(DATABASE_URI)
        return engine
    except SQLAlchemyError as e:
        st.error(f"Error connecting to the database: {e}")
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

# Main Streamlit App
st.title('Database Architecture Viewer and Saver')

# Initialize the connection
engine = init_connection()

if engine:
    # Get the database architecture
    architecture = get_database_architecture(engine)
    
    if architecture:
        # Schema selection
        schema_names = list(architecture.keys())
        selected_schema = st.selectbox("Select a schema", schema_names)
        
        if selected_schema:
            # Display and store all tables and columns in the selected schema
            selected_info = {selected_schema: architecture[selected_schema]}
            
            for table, columns in architecture[selected_schema].items():
                st.subheader(f"Table: {table}")
                st.write("Columns:")
                for col_name, col_type in columns.items():
                    st.write(f" - {col_name}: {col_type}")

            # Button to save the selected architecture as a JSON file
            if st.button("Save All Tables in Selected Schema as JSON"):
                try:
                    with open(f"{selected_schema}_architecture.json", "w") as json_file:
                        json.dump(selected_info, json_file, indent=4)
                    st.success(f"All tables in schema '{selected_schema}' saved as '{selected_schema}_architecture.json'.")
                except Exception as e:
                    st.error(f"Error saving JSON file: {e}")
