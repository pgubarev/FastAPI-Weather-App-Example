from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from conf.api_config import MINIMAL_SEARCH_LENGTH
from db import AsyncSession
from db.models import City

from .models import CitiesListResponseModel


router = APIRouter(tags=['cities'])


@router.get('/cities/', response_model=List[CitiesListResponseModel])
async def cities(search: str):
    """ Returns list of available cities """
    if not search or len(search) < MINIMAL_SEARCH_LENGTH:
        msg = (f'search string length must be '
               f'greater than or equal to {MINIMAL_SEARCH_LENGTH}')
        raise HTTPException(status_code=400, detail=msg)

    async with AsyncSession() as session:
        async with session.begin():
            db_request = select(
                City.id, City.name, City.country_code, City.lat, City.lon,
            ).where(
                City.name.ilike(f'%{search}%'),
            )
            results = await session.execute(db_request)
            return results.all()
