from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from starlette import status

from api.authentication_schemas import current_user_data
from api.exceptions import BadRequest
from db import db_session

from services.weather import WeatherService


router = APIRouter(tags=['weather'])


@router.get('/weather/{city_id}/current/')
async def current_weather(city_id: int, _: dict = current_user_data):
    async with db_session() as session:
        weather_service = WeatherService(session)
        try:
            weather_info = await weather_service\
                .get_current_weather_for_city(city_id)

        except WeatherService.InvalidCityId:
            raise BadRequest(detail='invalid city id')

        except WeatherService.DataServiceException as ex:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=ex.detail,
            )

        return weather_info


@router.get('/weather/{city_id}/forecast/')
async def current_weather(city_id: int, _: dict = current_user_data):
    async with db_session() as session:
        weather_service = WeatherService(session)
        try:
            weather_info = await weather_service\
                .get_forecast_weather_for_city(city_id)

        except WeatherService.InvalidCityId:
            raise BadRequest(detail='invalid city id')

        except WeatherService.DataServiceException as ex:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=ex.detail,
            )

        return weather_info
