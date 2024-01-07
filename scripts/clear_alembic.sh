mysql -h 127.0.0.1 -u fastapi -pfastapi fastapi -e "drop table alembic_version;"
mysql -h 127.0.0.1 -u fastapi -pfastapi fastapi -e "drop table votes;"
mysql -h 127.0.0.1 -u fastapi -pfastapi fastapi -e "drop table posts;"
mysql -h 127.0.0.1 -u fastapi -pfastapi fastapi -e "drop table users;"
rm -rf alembic
alembic init alembic
cp /tmp/alembic/script.py.mako alembic/script.py.mako
cp /tmp/alembic/env.py alembic/env.py
alembic revision --autogenerate
