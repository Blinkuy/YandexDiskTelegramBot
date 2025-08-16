from database import engine, Cafe
from sqlalchemy import insert, values

cafes = [
  {"title": "Читаешь",
  "secret_code": "ч0"}
]

def create_cafes(cafes):
    smtm = insert(Cafe).values(cafes)
    
    with engine.connect() as conn:
        conn.execute(smtm)
        conn.commit()

create_cafes(cafes)
 