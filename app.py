from fastapi import FastAPI, Request
import streamlit as st
import requests
import json
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/bfhl")
async def get_operation_code():
    response = {
        "operation_code": 1
    }
    return response

@app.post("/bfhl")
async def process_request(request: Request):
    body = await request.json()
    user_id = body.get("user_id", "")
    college_email = body.get("college_email", "")
    college_roll_number = body.get("college_roll_number", "")
    numbers = body.get("numbers", [])
    alphabets = body.get("alphabets", [])

    lowercase_alphabets = [char for char in alphabets if char.islower()]
    highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

    response = {
        "status": "success",
        "user_id": user_id,
        "college_email": college_email,
        "college_roll_number": college_roll_number,
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": highest_lowercase_alphabet
    }

    return response

def process_data(data):
    url = "http://localhost:8000/bfhl"  # Local URL for testing
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        return {"error": "Failed to process the data"}

def render_response(response_data):
    if "error" in response_data:
        st.error(response_data["error"])
    else:
        st.json(response_data)

def main():
    st.title("Bajaj Finserv Health Challenge")

    user_id = st.text_input("User ID")
    college_email = st.text_input("College Email")
    college_roll_number = st.text_input("College Roll Number")
    numbers = st.text_area("Numbers (comma separated)").split(',')
    alphabets = st.text_area("Alphabets (comma separated)").split(',')

    numbers = [int(num) for num in numbers if num.isdigit()]

    data = {
        "user_id": user_id,
        "college_email": college_email,
        "college_roll_number": college_roll_number,
        "numbers": numbers,
        "alphabets": alphabets
    }

    if st.button("Submit"):
        response_data = process_data(data)
        render_response(response_data)

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)).start()
    main()
