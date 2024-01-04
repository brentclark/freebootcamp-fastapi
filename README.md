# freebootcamp-fastapi
## Some python commands
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

python3 -m pip freeze > requirements.txt

sqlite3 create_database.db < create_database.sql

uvicorn app.main:app --reload

python3 -m pip list -o | awk '{if(NR>=3)print}'
python3 -m pip list -o | awk '{if(NR>=3)print}' | cut -d' ' -f1 | xargs -n1 python3 -m pip install --upgrade --force-reinstall
```

## Docker Commnand

```
docker build -t my-freebootcamp-fastapi-app . 
docker run -it -p 8000:8000 --rm --name my-freebootcamp-fastapi-app my-freebootcamp-fastapi-app

docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app up
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app logs -f
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app down
```

## Create a app/.env file with the following ENV variables for docker compose.

```
SQLALCHEMY_DATABASE_URL = "sqlite:///./posts.db"
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```
