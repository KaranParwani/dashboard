import os

import uvicorn
from dotenv import load_dotenv
from jose import JWTError
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from patient.routes.admin import admin_router
from patient.routes.chatbot import openai_router
from patient.routes.patient import patient_router

from config import HOST, PORT, ALLOW_ORIGINS
from patient.services.admin import add_super_admin
from patient.services.database import db_manager

app = FastAPI(title="Patient Assistant API")

# Load environment variables
load_dotenv(dotenv_path="config/.env")


@app.on_event("startup")
def startup_event():
    """Run database initialization and super admin creation at startup."""
    db_manager.connect()
    add_super_admin()


@app.exception_handler(JWTError)
async def handle_invalid_header_error(request, exc) -> JSONResponse:
    """Checks if the Header is invalid or not.

    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=422,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid header. Please chec k your JWT token.",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """To handle validation errors.

    :param request: The request object.
    :param exc: The exception object.
    """
    details = exc.errors()
    modified_details = []

    for error in details:
        if len(error["loc"]) == 1:
            modified_details = "Please provide body"
        else:
            modified_details.append(f"{error['loc'][1]} : {error['msg']}")

    response = {
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": modified_details,
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(response),
    )

# Middleware between Frontend and Backend``a
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_router, prefix="/patients", tags=["Patient"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(openai_router, prefix="/openai", tags=["Open AI"])


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))
