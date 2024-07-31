import streamlit as st
import requests

# Title of the app
st.title('Send Message to Flask API')

# Input for the message
message = st.text_input("Enter your message:")

# Display the entered message
st.write("Your message is:", message)

# Function to send the message to the Flask API
def send_to_flask_api(message):
    api_url = "http://127.0.0.1:5000/receive-message"  # Replace with your Flask API URL
    payload = {"message": message}
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        
        st.write("Response from Flask API:")
        st.write(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to send message to Flask API. Error: {e}")


# Button to send the message
if st.button("Send"):
    if message:
        send_to_flask_api(message)
    else:
        st.error("Please enter a message before sending.")
