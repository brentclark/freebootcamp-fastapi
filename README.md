# freebootcamp-fastapi

Run
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

python3 -m pip freeze > requirements.txt

sqlite3 create_database.db < create_database.sql

uvicorn app.main:app --reload