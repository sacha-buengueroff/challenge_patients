from fastapi import FastAPI, Request
from pydantic import ValidationError
from project.app.api.routers.patients import router as patients_router
from project.app.resources.response_maker import ResponseMaker

app = FastAPI(title="Light-It Challenge API")

app.include_router(patients_router)


@app.exception_handler(ValidationError)
async def value_error_exception_handler(request: Request, exc: ValidationError):
    return ResponseMaker.format_error(error=exc, method=request.method)


@app.get("/")
async def root():
    print("API Running")
    return {"message": "API running"}
