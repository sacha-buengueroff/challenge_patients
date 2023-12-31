from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy.orm import Session
from project.app.api.schemas.request_schemas import Patient as PatientSchema
from project.app.db.models import Patient

from project.app.db.connection import get_session


class PatientsRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def post_patient(self, document, patient: PatientSchema):
        """
        Adds a patient into the DB

        Args:
            document (bytes): document photo in bytes
            patient (PatientSchema): patient data in schema format

        Returns:
            pateitn: patient data in schema format
        """
        db_patient = Patient(
            name=patient.name,
            email=patient.email,
            address=patient.address,
            phone=patient.phone,
            document=document,
        )
        self.session.add(db_patient)
        self.session.commit()
        return patient

    def get_patients(self):
        """
        Gets all patient data from DB

        Returns:
            patients: list of dicts with patients data
        """
        statement = Select(Patient.name, Patient.email, Patient.address, Patient.phone)
        patients = self.session.execute(statement).mappings().all()
        patients = [dict(patient) for patient in patients]
        return patients
