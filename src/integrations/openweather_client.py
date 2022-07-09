import httpx


class OpenWeatherApiClient:
    class OpenWeatherAPiError(Exception):
        pass

    URL_TEMPLATE = 'https://api.openweathermap.org/data/2.5/{}'
    CURRENT_ENDPOINT = 'weather'
    FORECAST_ENDPOINT = 'forecast'

    def __init__(self, api_key: str):
        super().__init__()
        self._api_key = api_key

    async def get_current_info(self, lat: float, lon: float) -> dict:
        return await self._send_request(self.CURRENT_ENDPOINT, lat=lat, lon=lon)

    async def get_forecast_info(self, lat: float, lon: float) -> dict:
        return await self._send_request(self.FORECAST_ENDPOINT, lat=lat, lon=lon)

    async def _send_request(self, endpoint, **params) -> dict:
        url = self.URL_TEMPLATE.format(endpoint)
        query_params = {
            'appid': self._api_key,
            'units': 'metric',
            'lang': 'en',
            **params,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=query_params)
            except httpx.HTTPError as ex:
                msg = 'problem with sending request'
                raise self.OpenWeatherAPiError(msg) from ex

        if not response.status_code == httpx.codes.OK:
            msg = f'unexpected status code: {response.status_code}'
            raise self.OpenWeatherAPiError(msg)

        return response.json()
