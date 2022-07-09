from datetime import datetime
from typing import Tuple, List

from sqlalchemy.future import select

from cache import cache
from conf import settings
from db.models import City
from integrations import OpenWeatherApiClient

from .base import BaseDataAccessService


class WeatherService(BaseDataAccessService):
    class InvalidCityId(Exception):
        pass

    CACHE_KEY_TEMPLATE = '{}_weather_{}'
    CACHE_EXPIRATION_SECONDS = 60

    async def get_current_weather_for_city(self, city_id: int) -> dict:
        cache_key = self.CACHE_KEY_TEMPLATE.format('current', city_id)
        cached_results = await cache.get_cached_data(cache_key)
        if cached_results:
            return cached_results

        lat, lon = await self._get_position(city_id)

        open_weather_clint = \
            OpenWeatherApiClient(settings.OPEN_WEATHER_API_KEY)
        try:
            raw_data = await open_weather_clint.get_current_info(lat, lon)
        except OpenWeatherApiClient.OpenWeatherAPiError as ex:
            raise self.DataServiceException from ex

        data = self._extract_info_from_raw_data(raw_data)

        await cache.cache_data(cache_key, data, self.CACHE_EXPIRATION_SECONDS)

        return data

    async def get_forecast_weather_for_city(self, city_id: int) -> List[dict]:
        cache_key = self.CACHE_KEY_TEMPLATE.format('forecast', city_id)
        cached_results = await cache.get_cached_data(cache_key)
        if cached_results:
            return cached_results

        lat, lon = await self._get_position(city_id)

        open_weather_clint = \
            OpenWeatherApiClient(settings.OPEN_WEATHER_API_KEY)
        try:
            raw_data = await open_weather_clint.get_forecast_info(lat, lon)
        except OpenWeatherApiClient.OpenWeatherAPiError as ex:
            raise self.DataServiceException from ex

        data = [self._extract_info_from_raw_data(item)
                for item in raw_data['list']]

        await cache.cache_data(cache_key, data, self.CACHE_EXPIRATION_SECONDS)

        return data

    async def _get_position(self, city_id: int) -> Tuple[float, float]:
        db_request = select(City.lat, City.lon).where(
            City.id == city_id,
        ).limit(1)
        results = await self.session.execute(db_request)
        results = results.all()
        if len(results) == 0:
            raise self.DataServiceException('invalid city id')

        return results[0].lat, results[0].lon

    @classmethod
    def _extract_info_from_raw_data(cls, raw_data: dict) -> dict:
        return {
            'temperature': raw_data['main']['temp'],
            'feels_like_temperature': raw_data['main']['feels_like'],
            'wind_speed': raw_data['wind']['speed'],
            'rain_volume': (raw_data['rain'].get('3h', 0.0)
                            if 'rain' in raw_data else 0.0),
            'snow_volume': (raw_data['snow'].get('3h', 0.0)
                            if 'snow' in raw_data else 0.0),
            'timestamp': (raw_data['dt_txt'] if 'dt_txt' in raw_data
                          else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
