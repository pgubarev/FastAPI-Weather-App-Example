from fastapi import FastAPI
import uvicorn

from api import setup_api
from conf.api_config import API_PREFIX

from db import setup_database


app = FastAPI(title='FastAPI Weather App', docs_url=f'{API_PREFIX}/swagger',
              redoc_url=None,)

# Run setup functions
setup_database(app)
setup_api(app)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1')
