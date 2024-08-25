import subprocess
import threading
from fastapi import FastAPI, Request
import uvicorn
import streamlit as st
import requests
import json

# FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}

@app.post("/")
async def process_request(request: Request):
    # Get the request body
    body = await request.json()

    # Extract the required data from the request body
    data = body.get("data", [])
    numbers = [item for item in data if item.isdigit()]
    alphabets = [item for item in data if item.isalpha()]
    lowercase_alphabets = [char for char in alphabets if char.islower()]
    highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

    # Prepare the response
    response = {
        "is_success": True,
        "user_id": "john_doe_17091999",  # Replace with dynamic user info as needed
        "email": "john@xyz.com",  # Replace with dynamic email as needed
        "roll_number": "ABCD123",  # Replace with dynamic roll number as needed
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else []
    }

    return response

# Function to run FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Function to run Streamlit
def run_streamlit():
    # Streamlit app
    def process_data(data):
        # Send a POST request to the backend API
        url = "http://localhost:8000/"  # Backend API URL
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to process the data"}

    def render_response(response_data, selected_option):
        if "error" in response_data:
            st.error(response_data["error"])
        else:
            st.success("Data processed successfully!")
            if selected_option == "Alphabets & Numbers":
                st.write("Alphabets and Numbers:")
                st.write("Alphabets:", response_data.get("alphabets", []))
                st.write("Numbers:", response_data.get("numbers", []))
            elif selected_option == "Highest Lowercase Alphabet":
                st.write("Highest Lowercase Alphabet:")
                st.write(response_data.get("highest_lowercase_alphabet", []))

    def main():
        st.set_page_config(page_title="21BCE5542")

        st.markdown(
            """
            <style>
            .stApp {
                background-color: #D3D3D3;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.header("Bajaj Finserv Health Challenge: By Aastha Tiwari")
        st.markdown("<h1 style='text-align: center; color: red;'>21BCE5542</h1>", unsafe_allow_html=True)

        input_data = st.text_area("Enter JSON data", placeholder='{"data": ["A", "C", "z"]}')

        options = ["Alphabets & Numbers", "Highest Lowercase Alphabet"]
        selected_option = st.selectbox("Select an option", options)

        if st.button("Process Data"):
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
                return

            response = process_data(data)
            render_response(response, selected_option)

    if __name__ == "__main__":
        main()

# Run FastAPI in a separate thread
api_thread = threading.Thread(target=run_fastapi)
api_thread.daemon = True
api_thread.start()

# Run Streamlit app
run_streamlit()
