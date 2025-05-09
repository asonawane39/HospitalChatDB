from pydantic import BaseModel

class CaseModel(BaseModel):
    CASE_ID: str
    DESCRIPTION: str
    STATUS: str
    PRESCRIPTION: bool
    LABWORK: bool
    PATIENT_ID: str
    DOCTOR_ID: str