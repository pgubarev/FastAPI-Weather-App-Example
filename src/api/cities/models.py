from pydantic import BaseModel


class CitiesListResponseModel(BaseModel):
    id: int
    name: str
    country_code: str
    lat: float
    lon: float
