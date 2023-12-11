from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Request,
    UploadFile,
)

from project.app.api.schemas.request_schemas import Patient
from project.app.resources.notifications import NotificationSender
from project.app.repositories.patients_repository import PatientsRepository
from project.app.resources.response_maker import ResponseMaker


router = APIRouter(prefix="/patients", tags=["Patients 🏥"])


@router.post("/", summary="Creates a patient")
async def post_patient(
    request: Request,
    background_tasks: BackgroundTasks,
    patient: Patient = Depends(),
    document: UploadFile = File(...),
    repo: PatientsRepository = Depends(PatientsRepository),
):
    """
    Creates a patient with all the information:

    - **name**: patient name
    - **email**: patient email
    - **address**: patient address
    - **phone**: patient phone number
    - **document**: patients document photo

    Returns a dict with all the patient data
    """
    try:
        assert document.content_type.startswith("image"), "Invalid file type"
        document = await document.read()
        response = ResponseMaker.format(
            results=repo.post_patient(document=document, patient=patient),
            method=request.method,
        )
        if response.status_code == 200:
            background_tasks.add_task(NotificationSender.send_email, patient.email)
            # Placeholder for SMS Notification
            # background_tasks.add_task(NotificationSender.send_sms, patient.phone)
        return response
    except Exception as e:
        return ResponseMaker.format_error(error=e, method=request.method)


@router.get("/", summary="Gets all patients")
def get_patients(
    request: Request, repo: PatientsRepository = Depends(PatientsRepository)
):
    """
    Gets all the patients in the DB.

    Returns a list of dicts with all the patients data.
    """
    try:
        return ResponseMaker.format(results=repo.get_patients(), method=request.method)
    except Exception as e:
        return ResponseMaker.format_error(error=e, method=request.method)
