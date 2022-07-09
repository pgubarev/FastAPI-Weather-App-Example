from pydantic import BaseModel, validator

from .validators import email_validator, greater_than_zero_validator


class RegistrationRequestModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    city_id: int
    password: str

    # validators
    _email_validator = validator('email', allow_reuse=True)(email_validator)
    _city_id_validator = validator('city_id', allow_reuse=True)(greater_than_zero_validator)  # noqa: E501


class RegistrationResponseModel(BaseModel):
    email: str
    first_name: str
    last_name: str


class ConfirmRegistrationModel(BaseModel):
    email: str
    code: str

    # validators
    _email_validator = validator('email', allow_reuse=True)(email_validator)


class LoginRequestModel(BaseModel):
    email: str
    password: str

    # validators
    _email_validator = validator('email', allow_reuse=True)(email_validator)


class JWTResponse(BaseModel):
    jwt: str
