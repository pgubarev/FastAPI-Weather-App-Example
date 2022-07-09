from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette import status


async def validation_exception_handler(_request: Request,
                                       exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"errors": exc.errors()}),
    )


async def default_exception_handler(_request: Request,
                                    exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"errors": [exc.detail]})
    )


EXCEPTION_HANDLERS_LIST = [
    (RequestValidationError, validation_exception_handler),
    (HTTPException, default_exception_handler),
]
