import requests
import os
import json
import uvicorn
from dotenv import load_dotenv
from utils.get_data import load_data
from utils.db_CRUD import query_sql_db, query_mongo_db
from utils.db_connecter import connect_to_mysql, connect_to_mongodb
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]



class QueryModel(BaseModel):
    query: str

class ResponseModel(BaseModel):
    message: str
    status: str
    data: list | dict
    response_length: str
    dataheaders: list

def get__query__from__llm(task):
    """
    This fuction is used to generate the query that will be used to query the databases
    """
    API_KEY = os.getenv("GEMINI_API_KEY")
    URL = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key="
        + API_KEY
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": """You are working with 3 databases:

                                1. HOSPITAL (SQL Database):
                                - Tables:
                                    - MED_CASE(CASE_ID, DESCRIPTION, STATUS, LABWORK, PRESCRIPTION, PATIENT_ID, DOCTOR_ID)
                                    - DOCTOR(DOCTOR_ID, FIRST_NAME, LAST_NAME, EMAIL, CONTACT_NUMBER, SPECIALIZATION)
                                    - PATIENT(PATIENT_ID, FIRST_NAME, LAST_NAME, DOB, SEX, ADDRESS, PHONE_NUMBER, BLOOD)

                                2. CASE_APPOINTMENTS (MongoDB Database):
                                - Collections:
                                    - APPOINTMENTS(appointment_id, appointment_date, appointment_time, case_id)
                                    - CASE(case_id, description, status, labwork, prescription, patient_id, doctor_id)

                                3. CASE_PRESCRIPTIONS (MongoDB Database):
                                - Collections:
                                    - CASE(case_id, description, status, labwork, prescription, patient_id, doctor_id)
                                    - PRESCRIPTION(prescription_id, case_id)
                                    - MEDICINE(medicine_id, medicine_name)
                                    - PRESCRIPTION_ITEMS(prescription_id, sr_no, medicine_id, quantity)

                                Your task is to """ + task + """Your output must be a JSON object with the following fields:

                                - "query": the query to be executed (in SQL or PyMongo syntax, based on dbtype)
                                - "dbname": the name of the database
                                - "tablename": the table (for SQL) or collection (for MongoDB)
                                - "dbtype": one of ["SQL", "NoSQL"]
                                - "dataheaders": the list of field/column names that the query will return
                                - "response_length": "single" if 1 record is returned, "multiple" if multiple records are returned

                                Rules:
                                - If the task is about doctors or patients, always use the SQL database (HOSPITAL).
                                - If the task is about appointments, always use the NoSQL database (CASE_APPOINTMENTS).
                                - If the task is about prescriptions, always use the NoSQL database (CASE_PRESCRIPTIONS).
                                - When dbtype is "NoSQL", generate **PyMongo query syntax** (use find, aggregate, or lookup).
                                - Do not use SQL syntax for NoSQL databases.
                                - Return only the JSON response. No explanation or extra text.

                                # give me pymongo queries like this, "result = db.query" and make this as can be executable in a python exec("") str don't add any newline characters just give a online 

                        

                                Be precise with syntax for each type of database."""}
                ],
            }
        ]
    }
    response = requests.post(URL, headers=headers, json=data)
    response_json = response.json()
    return dict(response_json)['candidates'][0]['content']['parts'][0]['text'].strip()

# server function that are async...
server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@server.get('/server/test')
def test():
    return {
        "message": "Server Running...."
    }

    
# @server.post('/server/get_response')
# def get_response(data: QueryModel):
#         response = get__query__from__llm(data.query)
#         data = json.loads(response[response.index("{"):-3])
#         if data['dbtype'] == 'SQL':
#             conn = connect_to_mysql(data['dbname'])
#             return { "response" : f"{query_sql_db(conn, data)}" }
#         elif data['dbtype'] == 'NoSQL':
#             client = connect_to_mongodb(data['dbname'])
#             return { "response": f"{(query_mongo_db(client, data))}"}

@server.post('/server/get_response')
def get_response(data: QueryModel):
    # print("*\n" *100 )
    # return JSONResponse(content={"response": "called from frontend!!"})
    response = get__query__from__llm(data.query)
    
    try:
        # Parse the JSON object from response
        data_json = json.loads(response[response.index("{"):-3])
    except Exception as e:
        return JSONResponse(content={"error": "Failed to parse response", "details": str(e)}, status_code=400)

    if data_json.get('dbtype') == 'SQL':
        conn = connect_to_mysql(data_json['dbname'])
        result = query_sql_db(conn, data_json)
    elif data_json.get('dbtype') == 'NoSQL':
        client = connect_to_mongodb(data_json['dbname'])
        result = query_mongo_db(client, data_json)
    else:
        return JSONResponse(content={"error": "Unsupported database type"}, status_code=400)

    return JSONResponse(content={"response": result})

def run_as_server():
    """
    Allows the application to be used as serverside
    """
    uvicorn.run("main:server", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("main:server", host="192.168.1.1", port=8000, reload=True)


def run_in_console():
    print("[*] Hey I'm Donna, Tell me how can i help you today!!")
    while True:
        task = input("[*] You: ").lower()
        if task == 'bye':
            print("[*] GoodBye!!")
            break

        response = get__query__from__llm(task)
        data = json.loads(response[response.index("{"):-3])
        print(data)
        print(data['dbtype'])
        if data['dbtype'] == 'SQL':
            conn = connect_to_mysql(data['dbname'])
            print(query_sql_db(conn, data)) 
        elif data['dbtype'] == 'NoSQL':
            client = connect_to_mongodb(data['dbname'])
            print(query_mongo_db(client, data))

if __name__ == "__main__":
    load_data()

    res = input("[*] DO YOU WANT TO RUN IN (1). SERVER OR (2). CONSOLE, ")
    if res == '1':
        run_as_server()
    elif res == '2':
        run_in_console()
