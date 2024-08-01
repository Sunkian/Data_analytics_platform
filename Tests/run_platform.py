# app.py
import streamlit as st
import pandas as pd
from connection_database import connect_to_mysql, execute_sql_query, get_database_architecture
import json
# Main Streamlit App
st.title('Database Analytics Platform')



# Connect to the database
engine = connect_to_mysql()

if engine:
    
    # === Select the database Schema and save its architecture as a .json file ===
    st.markdown('''
    :blue[First, select your Schema]
    ''')
    architecture = get_database_architecture(engine)
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

        if st.button("Select this database"):
            try: 
                with open(f"{selected_schema}_architecture.json", "w") as json_file:
                        json.dump(selected_info, json_file, indent=4)
                st.success(f"All tables in schema '{selected_schema}' saved as '{selected_schema}_architecture.json'.")
            except Exception as e:
                st.error(f"Error saving JSON file: {e}")



    st.markdown('''
    :blue[Then, choose your database type and specify the query you wish to ask the model to translate]
    ''')
    # === Here, enter the NLP query you wish to ask the model to translate ===
    # Input for the query
    # Input field for selecting the database format
    db_format = st.selectbox("Select your database format:", 
                            ["MySQL", "PostgreSQL", "Snowflake", "SQLite", "Microsoft SQL Server"])
    query = st.text_input("Query")
    context = [db_format, query]

    if st.button("Send to LLM"):
            try: 
                with open("prompt_context.json", "w") as json_file:
                        json.dump(context, json_file, indent=4)
                st.success("Saving your context locally")
            except Exception as e:
                st.error(f"Error saving JSON file: {e}")
    

    st.markdown('''
    :blue[If you are okay with the translation, search the database !]
    ''')


    st.markdown('''
    :blue[Test : write an SQL query to send the database]
    ''')
    # Input for the SQL query
    sql_query = st.text_area("Enter your SQL query:")
    
    # Button to execute the SQL query
    if st.button("Execute"):
        if sql_query.strip():
            # Execute the SQL query
            query_results = execute_sql_query(engine, sql_query)
            
            if query_results:
                # Display the results as a DataFrame
                df = pd.DataFrame(query_results)
                st.write("Query Results:")
                st.dataframe(df)
        else:
            st.error("Please enter a SQL query before executing.")