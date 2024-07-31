import streamlit as st

st.title('Database Schema Input Form')

# Section for Database Information
st.header("Database Information")
database_name = st.text_input("Enter your database name", "my_database")

# Section for Tables
st.header("Tables")
num_tables = st.number_input("Number of tables", min_value=1, max_value=10, value=1)

# Placeholder to dynamically create input fields for each table
table_info = []
for i in range(num_tables):
    st.subheader(f"Table {i + 1}")
    table_name = st.text_input(f"Table {i + 1} Name", f"table_{i + 1}")
    schema_name = st.text_input(f"Schema for Table {i + 1}", f"schema_{i + 1}")
    num_columns = st.number_input(f"Number of columns in {table_name}", min_value=1, max_value=50, value=1)

    columns = []
    for j in range(num_columns):
        col_name = st.text_input(f"Column {j + 1} Name", f"column_{j + 1}", key=f"col_{i}_{j}_name")
        col_type = st.text_input(f"Column {j + 1} Type", f"VARCHAR(255)", key=f"col_{i}_{j}_type")
        col_constraints = st.text_input(f"Column {j + 1} Constraints", "", key=f"col_{i}_{j}_constraints")
        columns.append({"name": col_name, "type": col_type, "constraints": col_constraints})
    
    table_info.append({"table_name": table_name, "schema_name": schema_name, "columns": columns})

# Button to submit data
if st.button("Submit"):
    # Here, you could save the data to a file, database, or perform other actions
    st.success("Database schema information submitted successfully!")

    # Display the entered data
    st.subheader("Entered Database Information")
    st.write(f"**Database Name:** {database_name}")
    for table in table_info:
        st.write(f"**Table Name:** {table['table_name']}")
        st.write(f"**Schema Name:** {table['schema_name']}")
        st.write("**Columns:**")
        for column in table["columns"]:
            st.write(f" - {column['name']} ({column['type']}), Constraints: {column['constraints']}")
