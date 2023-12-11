from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy.orm import Session
from project.app.api.schemas.request_schemas import Patient as PatientSchema
from project.app.db.models import Patient

from project.app.db.connection import get_session


class TestPatientsRepository:
    __test__ = False

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def post_patient(self, document, patient: PatientSchema):
        db_patient = Patient(
            name=patient.name,
            email=patient.email,
            address=patient.address,
            phone=patient.phone,
            document=document,
        )
        self.session.add(db_patient)
        return patient

    def get_patients(self):
        statement = Select(Patient.name, Patient.email, Patient.address, Patient.phone)
        patients = self.session.execute(statement).mappings().all()
        patients = [dict(patient) for patient in patients]
        return patients
