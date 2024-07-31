import streamlit as st

# Title of the app
st.title('Database Schema Input Form')

# Input for the database name
database_name = st.text_input("Enter the name of your database:")

# Initialize session state for tables
if 'tables' not in st.session_state:
    st.session_state.tables = []

# Function to add a new table
def add_table():
    st.session_state.tables.append({
        "table_name": "",
        "schema_name": "",
        "columns": []
    })

# Function to add a new column to a table
def add_column(table_index):
    st.session_state.tables[table_index]["columns"].append({
        "column_name": "",
        "data_type": "",
        "is_nullable": False
    })

# Display the form for each table
for i, table in enumerate(st.session_state.tables):
    st.subheader(f"Table {i+1}")
    table["table_name"] = st.text_input(f"Table {i+1} Name:", value=table["table_name"])
    table["schema_name"] = st.text_input(f"Schema Name for Table {i+1}:", value=table["schema_name"])

    # Display the form for each column
    for j, column in enumerate(table["columns"]):
        with st.expander(f"Column {j+1}"):
            column["column_name"] = st.text_input(f"Column {j+1} Name:", value=column["column_name"])
            column["data_type"] = st.text_input(f"Data Type for Column {j+1}:", value=column["data_type"])
            column["is_nullable"] = st.checkbox(f"Is Column {j+1} Nullable?", value=column["is_nullable"])

    # Button to add a new column
    if st.button(f"Add Column to Table {i+1}"):
        add_column(i)

# Button to add a new table
if st.button("Add Table"):
    add_table()

# Display the entered data
if st.session_state.tables:
    st.subheader("Entered Data")
    st.write(st.session_state.tables)

# Display the database name
if database_name:
    st.subheader("Database Name")
    st.write(database_name)