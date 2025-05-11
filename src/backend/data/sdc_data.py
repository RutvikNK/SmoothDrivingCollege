from pydantic import BaseModel
from enum import Enum

class MeetingType(Enum):
    LESSON = "Lesson"
    WRITTEN_EXAM = "Exam: Written"
    DRIVING_EXAM = "Exam: Behind the Wheel"

class Office(BaseModel):
    office_street_address: str
    office_city: str
    office_council_area: str
    office_postal_code: str

class Employee(BaseModel):
    emp_name: str
    emp_gender: str
    emp_email: str
    emp_phone_no: str
    emp_manager_id: int

class Interview(BaseModel):
    interv_client_id: int
    interv_inst_id: int
    interv_location_id: int
    interv_location: str
    interv_date: str

class Meeting(BaseModel):
    meeting_client_id: int
    meeting_inst_id: int
    meeting_vehicle_no: str
    meeting_location_id: int
    meeting_location: str
    meeting_start: str
    meeting_end: str
    meeting_type: str
    meeting_notes: str = ""
    meeting_mileage: int = 0

class Client(BaseModel):
    client_name: str
    client_gender: str
    client_phone_no: str
    client_email: str
    client_inst_id: int
    client_emergency_contact_name: str
    client_emergency_contact_phone: str
    client_interviewed: bool = False
    client_age: int

class Vehicle(BaseModel):
    vehicle_license_no: str
    vehicle_make: str
    vehicle_model: str
    vehicle_year: str
    vehicle_color: str
    vehicle_last_inspection: str
