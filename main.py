import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import HOST, PORT

app = FastAPI(title="Patient Assistant API")


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
            "message": "Invalid header. Please check your JWT token.",
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


# To allow API calls from
origins = [
    "http://localhost:5173",
]


# Middleware between Frontend and Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))
