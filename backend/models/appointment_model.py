from pydantic import BaseModel

class AppointmentModel(BaseModel):
    appointment_id: str
    appointment_date: str 
    appointment_time: str
    case_id: str