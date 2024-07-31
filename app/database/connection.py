import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Configuration
user = 'root'
password = '@Freestyle678'  # Password with special characters
host = 'localhost'
database = 'platform'

# URL-encode the password
encoded_password = quote_plus(password)

# Construct the database URI
DATABASE_URI = f'mysql+pymysql://{user}:{encoded_password}@{host}/{database}'

# Function to connect to the MySQL database using SQLAlchemy
def connect_to_mysql():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

# Function to execute a SQL query and fetch the result using SQLAlchemy
def execute_query(session, query):
    result = session.execute(text(query))
    session.commit()
    return result.fetchall()

# Streamlit app
st.title('SQL Command Executor')

# Connect to the database
try:
    session, engine = connect_to_mysql()
    st.success("Connected to the MySQL database!")
    
    # User input for SQL command
    sql_command = st.text_area('Enter your SQL command:')
    
    if st.button('Execute'):
        if sql_command:
            try:
                # Execute the SQL command
                result = execute_query(session, sql_command)
                st.write("Query Result:")
                for row in result:
                    st.write(row)
            except Exception as e:
                st.error(f"Error executing the query: {e}")
        else:
            st.warning('Please enter a SQL command.')
    
    # Close the session
    session.close()
    engine.dispose()
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
