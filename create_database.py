from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: SQLModel.String(max_length=64)
    price: SQLModel.Float(4,4)
    is_sale: SQLModel.Boolean(default=True)

hero_1 = Products(name="Deadpond", price=1.2)
hero_2 = Products(name="Deadpond", price=1.2)
hero_3 = Products(name="Deadpond", price=1.2)

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()


with Session(engine) as session:
    statement = select(Products).where(Products.name == "Deadpond")
    hero = session.exec(statement).first()
    print(hero)
