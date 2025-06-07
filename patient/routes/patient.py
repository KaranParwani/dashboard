from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette import status

from config import SECRET_KEY, ALGORITHM
from patient.schemas.patient import PatientRecord, UpdatePatientRecord
from patient.services.admin import AdminAuthenticator
from patient.services.database import db_manager
from patient.services.exceptions import AuthJWTException, response_structure
from patient.services.patient import PatientsManager

patient_router = APIRouter()


@patient_router.get("/")
async def get_patient_details(
    patient_id: int = None,
    session: Session = Depends(db_manager.get_database_session),
    authorization: str = Header(None),
):
    try:
        authenticate = AdminAuthenticator(session, SECRET_KEY, ALGORITHM)
        authenticate.authenticate_admin_token(authorization)

        patients = PatientsManager(session)

        if patient_id is not None:
            return await patients.get_patients_details(patient_id)
        else:
            return await patients.get_patients_details()

    except Exception as e:
        if isinstance(e, AuthJWTException):
            return e

        return response_structure(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None
        )


@patient_router.post("/")
async def add_patient_details(
    patient_details: PatientRecord,
    session: Session = Depends(db_manager.get_database_session),
    authorization: str = Header(None),
):
    try:
        authenticate = AdminAuthenticator(session, SECRET_KEY, ALGORITHM)
        authenticate.authenticate_admin_token(authorization)

        patients = PatientsManager(session, patient_details.model_dump())
        return await patients.add_patient_details()

    except Exception as e:
        if isinstance(e, AuthJWTException):
            return e

        return response_structure(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None
        )


@patient_router.put("/update")
async def update_patient_details(
    patient_details: UpdatePatientRecord,
    session: Session = Depends(db_manager.get_database_session),
    authorization: str = Header(None),
):

    try:
        authenticate = AdminAuthenticator(session, SECRET_KEY, ALGORITHM)
        admin_details = authenticate.authenticate_admin_token(authorization)

        patients = PatientsManager(session, patient_details.model_dump())
        return await patients.update_patients_details(admin_details.get("user_id"))

    except Exception as e:
        if isinstance(e, AuthJWTException):
            return e

        return response_structure(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None
        )


@patient_router.delete("/delete")
async def delete_patient_record(
    patient_id: int = None,
    session: Session = Depends(db_manager.get_database_session),
    authorization: str = Header(None),
):
    try:
        authenticate = AdminAuthenticator(session, SECRET_KEY, ALGORITHM)
        admin = authenticate.authenticate_admin_token(authorization)

        patients = PatientsManager(session)
        return await patients.delete_patient_record(patient_id, admin["user_id"])

    except Exception as e:
        if isinstance(e, AuthJWTException):
            return e

        return response_structure(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None
        )
