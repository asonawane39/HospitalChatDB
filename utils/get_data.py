# imports
import json 
import pandas as pd
from collections import namedtuple
from models.doctor_model import DoctorModel
from models.patient_model import PatientModel
from models.case_model import CaseModel
from models.appointment_model import AppointmentModel
from .db_connecter import connect_to_mysql, connect_to_mongodb
from sqlalchemy import text
import warnings
warnings.filterwarnings("ignore")


# JSON loader placeholder (not implemented yet)
def load_json_data(filename: str, dbname: str, tablename: str, model_type: str, sql_flag = 1):
    with open('../chatdb/data/' + filename, 'r') as data_file:
        data = json.load(data_file)
        if sql_flag == 0:
            client = connect_to_mongodb(f"{dbname}")
            collection = client[f'{tablename}']  
            for row in data:
                    collection.insert_one(row)

        

    # Implementation to parse and insert goes here


def load_csv_data(filename: str, dbname: str, tablename: str, model_type: str, sql_flag = 1):
    """
    This function loads data from CSV and inserts into the given table.
    """
    data = pd.read_csv('./data/' + filename)
    if sql_flag == 1:
        conn = connect_to_mysql('hospital')
        for _, row in data.iterrows():
            if model_type == "DoctorModel":
                doctor = DoctorModel(
                    DOCTOR_ID=str(row[0]).zfill(4),
                    FIRST_NAME=row[1],
                    LAST_NAME=row[2],
                    SPECIALIZATION=row[3],
                    CONTACT_NUMBER=str(row[4]),
                    EMAIL=row[5]
                )
                query = text(f"""
                    INSERT INTO {tablename} 
                    (DOCTOR_ID, FIRST_NAME, LAST_NAME, SPECIALIZATION, CONTACT_NUMBER, EMAIL)
                    VALUES (:id, :first, :last, :spec, :phone, :email)
                """)
                conn.execute(query, {
                    "id": doctor.DOCTOR_ID,
                    "first": doctor.FIRST_NAME,
                    "last": doctor.LAST_NAME,
                    "spec": doctor.SPECIALIZATION,
                    "phone": doctor.CONTACT_NUMBER,
                    "email": doctor.EMAIL
                })

            elif model_type == "PatientModel":
                patient = PatientModel(
                    PATIENT_ID=str(row[0]).zfill(6),
                    FIRST_NAME=row[1],
                    LAST_NAME=row[2],
                    DOB=str(row[3]),
                    SEX=row[4],
                    ADDRESS=row[5],
                    PHONE_NUMBER=str(row[6]),
                    BLOOD=row[7]
                )
                query = text(f"""
                    INSERT INTO {tablename}
                    (PATIENT_ID, FIRST_NAME, LAST_NAME, DOB, SEX, ADDRESS, PHONE_NUMBER, BLOOD)
                    VALUES (:id, :first, :last, :dob, :sex, :address, :phone, :blood)
                """)
              
                conn.execute(query, {
                    "id": patient.PATIENT_ID,
                    "first": patient.FIRST_NAME,
                    "last": patient.LAST_NAME,
                    "dob": patient.DOB,
                    "sex": patient.SEX,
                    "address": patient.ADDRESS,
                    "phone": patient.PHONE_NUMBER,
                    "blood": patient.BLOOD
                })

            elif model_type == "CaseModel":
                case_data = CaseModel(
                    CASE_ID=str(row[0]).zfill(7),
                    DESCRIPTION=str(row[1]),
                    STATUS=str(row[2]),
                    LABWORK=bool(row[3]),
                    PRESCRIPTION=bool(row[4]),
                    PATIENT_ID=str(row[5]).zfill(6),
                    DOCTOR_ID=str(row[6]).zfill(4)
                )
                query = text(f"""
                    INSERT INTO {tablename}
                    (CASE_ID, DESCRIPTION, STATUS, LABWORK, PRESCRIPTION, PATIENT_ID, DOCTOR_ID)
                    VALUES (:cid, :desc, :status, :lab, :presc, :pid, :did)
                """)
                conn.execute(query, {
                    "cid": case_data.CASE_ID,
                    "desc": case_data.DESCRIPTION,
                    "status": case_data.STATUS,
                    "lab": case_data.LABWORK,
                    "presc": case_data.PRESCRIPTION,
                    "pid": case_data.PATIENT_ID,
                    "did": case_data.DOCTOR_ID
                })
        conn.commit()
        conn.close()
    else:
        client = connect_to_mongodb(f"{dbname}")
        # db = client['CASE']  # MongoDB database
        collection = client[f"{tablename}"]          # Collection name (can be changed)
        for _, row in data.iterrows():
            if model_type == 'CaseModel':
                case_data = CaseModel(
                    CASE_ID=str(row[0]).zfill(7),
                    DESCRIPTION=str(row[1]),
                    STATUS=str(row[2]),
                    LABWORK=bool(row[3]),
                    PRESCRIPTION=bool(row[4]),
                    PATIENT_ID=str(row[5]).zfill(6),
                    DOCTOR_ID=str(row[6]).zfill(4)
                )

                # Convert namedtuple to dict
                document = {
                    "case_id": case_data.CASE_ID,
                    "description": case_data.DESCRIPTION,
                    "status": case_data.STATUS,
                    "labwork": case_data.LABWORK,
                    "prescription": case_data.PRESCRIPTION,
                    "patient_id": case_data.PATIENT_ID,
                    "doctor_id": case_data.DOCTOR_ID
                }

                # Insert into MongoDB collection
                collection.insert_one(document)
                print(f"Inserted Case {case_data.CASE_ID} into MongoDB.")

    

def load_data():
    option = input("[*] DO YOU WANT TO LOAD DATA INTO DATA BASE Y/N: ")
    if option.upper() == 'Y':
        LOAD_TYPE = namedtuple("LOAD_TYPE", ['filename', 'dbname', 'tablename', 'model_type', 'sql_flag'])

        csv_files = [
            LOAD_TYPE('doctor.csv', 'HOSPITAL', 'DOCTOR', "DoctorModel", 1),
            LOAD_TYPE('patient.csv', 'HOSPITAL', 'PATIENT', 'PatientModel', 1),
            LOAD_TYPE('case.csv', 'HOSPITAL', 'MED_CASE', 'CaseModel', 1),
            LOAD_TYPE('case.csv', 'CASE_APPOINTMENTS', 'CASE', 'CaseModel', 0),
            LOAD_TYPE('case.csv', 'CASE_PRESCRIPTIONS', 'CASE', 'CaseModel', 0),
        ]

        json_files = [
            LOAD_TYPE('appointments.json', 'CASE_APPOINTMENTS', 'APPOINTMENTS', 'AppointmentModel', 0),
            LOAD_TYPE('prescription.json', 'CASE_PRESCRIPTIONS', 'PRESCRIPTION', '', 0),
            LOAD_TYPE('prescription_items.json', 'CASE_PRESCRIPTIONS', 'PRESCRIPTION_ITEMS', '', 0),
            LOAD_TYPE('medicine.json', 'CASE_PRESCRIPTIONS', 'MEDICINE', '', 0),

        ]

        for csv_file in csv_files:
            load_csv_data(csv_file.filename, csv_file.dbname, csv_file.tablename, csv_file.model_type, csv_file.sql_flag)


        for json_file in json_files:
            load_json_data(json_file.filename, json_file.dbname, json_file.tablename, json_file.model_type, json_file.sql_flag)
    else:
        print("[*] IT SEEMS DATA ALREADY EXISTS....")