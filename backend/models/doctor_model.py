from pydantic import BaseModel

class DoctorModel(BaseModel):
    DOCTOR_ID: str
    FIRST_NAME: str 
    LAST_NAME: str
    EMAIL: str 
    CONTACT_NUMBER: str
    SPECIALIZATION: str
