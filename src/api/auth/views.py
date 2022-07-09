from fastapi import APIRouter
from starlette import status

from api.exceptions import BadRequest
from db import db_session

from api.jwt import create_jwt
from services.auth import AuthCodesService
from services.users import UsersService

from .models import (RegistrationRequestModel, RegistrationResponseModel,
                     ConfirmRegistrationModel, LoginRequestModel, JWTResponse)


router = APIRouter(tags=['auth'])


@router.post('/auth/registration/', status_code=status.HTTP_201_CREATED,
             response_model=RegistrationResponseModel)
async def registration(data: RegistrationRequestModel):
    async with db_session() as session:
        us = UsersService(session)
        if await us.is_user_exists(data.email):
            raise BadRequest('user already exists')

        user = await us.create_new_user(commit=False, **data.dict())

        confirmation_code = await AuthCodesService(session)\
            .create_confirmation_code_for_user(user)

        # TODO: send email with confirmation code
        return {
            'email': data.email,
            'first_name': data.first_name,
            'last_name': data.last_name,
        }


@router.post('/auth/confirm-email/')
async def confirm_email(data: ConfirmRegistrationModel):
    async with db_session() as session:
        auth_code_service = AuthCodesService(session)
        try:
            await auth_code_service.confirm_user_email(email=data.email,
                                                       code=data.code)
        except AuthCodesService.DataServiceException as ex:
            raise BadRequest(ex.detail)

    return {}


@router.post('/auth/login/', response_model=JWTResponse)
async def login(data: LoginRequestModel):
    async with db_session() as session:
        us = UsersService(session)
        user = await us.authenticate(data.email, data.password)
        if user is None:
            raise BadRequest('invalid email or password')

    jwt = create_jwt(user)
    return {'jwt': jwt}
