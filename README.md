# FastAPI Weather App

Example project with fully async web server.
Tech stack:
- Python 3.8
- FastAPI
- SQLAlchemy
- redis-py
- httpx


##### Project structure:

`conf` - contains settings for project and project-level constants;  
`api` - contains logic for api: views, models, auth classes and etc.;  
`cache` - contains utils for caching in application;
`db` - database client and SQLAlchemy models definitions;  
`intergrations` - contains integrations with third-party services;  
`services` - data access level, contains logic for working with cache and database.
   