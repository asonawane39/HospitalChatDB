from pydantic import BaseModel

class PatientModel(BaseModel):
    PATIENT_ID: str
    FIRST_NAME: str
    LAST_NAME: str
    DOB: str
    SEX: str
    ADDRESS: str 
    PHONE_NUMBER: str
    BLOOD: str