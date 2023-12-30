# freebootcamp-fastapi

Run
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

python3 -m pip freeze > requirements.txt

sqlite3 create_database.db < create_database.sql

uvicorn app.main:app --reload

python3 -m pip list -o | awk '{if(NR>=3)print}'
ython3 -m pip list -o | awk '{if(NR>=3)print}' | cut -d' ' -f1 | xargs -n1 python3 -m pip install --upgrade --force-reinstall

