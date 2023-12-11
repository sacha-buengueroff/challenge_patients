from fastapi.testclient import TestClient
from project.app.repositories.patients_repository import PatientsRepository
from project.app.repositories.test_patients_repository import TestPatientsRepository
from project.app.api.main import app
from PIL import Image
import io


client = TestClient(app)

app.dependency_overrides[PatientsRepository] = TestPatientsRepository


def test_post_patient():
    """
    Tests if patient is succesfully created in DB.
    """
    image = Image.new("RGB", (100, 100), "white")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="jpeg")
    image_bytes.seek(0)
    files = {"document": ("test.jpeg", image_bytes, "image/jpeg")}

    data = {
        "name": "Nombre Falso",
        "email": "email@falso.com",
        "address": "Address",
        "phone": "1111111111",
    }
    response = client.post("/patients", params=data, files=files)
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"


def test_get_patient():
    """
    Tests GET patients.
    """
    response = client.get("/patients")
    assert response.status_code == 200


def test_post_patient_wrong_format_mail():
    """
    Tests if there is an error when sending an incorrect email.
    """
    image = Image.new("RGB", (100, 100), "white")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="jpeg")
    image_bytes.seek(0)
    files = {"document": ("test.jpeg", image_bytes, "image/jpeg")}

    data = {
        "name": "Nombre Falso",
        "email": "emailfalsocom",
        "address": "Address",
        "phone": "1111111111",
    }

    response = client.post("/patients", params=data, files=files)
    print(response.content)
    assert response.status_code == 400
    assert response.json()["status"] == "FAIL"
    assert response.json()["error"]["description"].startswith(
        "1 validation error for Patient"
    )


def test_post_patient_wrong_format_phone():
    """
    Tests if there is an error when sending an incorrect phone number.
    """
    image = Image.new("RGB", (100, 100), "white")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="jpeg")
    image_bytes.seek(0)
    files = {"document": ("test.jpeg", image_bytes, "image/jpeg")}

    data = {
        "name": "Nombre Falso",
        "email": "emailfalsocom",
        "address": "Address",
        "phone": 1111111111,
    }

    response = client.post("/patients", params=data, files=files)
    assert response.status_code == 400
    assert response.json()["status"] == "FAIL"
    assert response.json()["error"]["description"].startswith(
        "1 validation error for Patient"
    )


def test_post_patient_invalid_file():
    """
    Tests if there is an error when sending an incorrect file.
    """
    text = "This is a dummy text file for testing."
    file = io.BytesIO(text.encode())
    files = {"document": ("dummy_file.txt", file)}

    data = {
        "name": "Nombre Falso",
        "email": "email@falso.com",
        "address": "Address",
        "phone": "1111111111",
    }

    response = client.post("/patients", params=data, files=files)
    print(response.content)
    assert response.status_code == 400
    assert response.json()["status"] == "FAIL"
    assert response.json()["error"]["description"] == "Invalid file type"
