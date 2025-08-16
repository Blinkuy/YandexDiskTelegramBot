from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Table, ForeignKey, MetaData, create_engine, insert, values, select

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    cafe_id: Mapped[int] = mapped_column(ForeignKey("cafes.id", ondelete="CASCADE"))

class Cafe(Base):
    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    secret_code: Mapped[str]

engine = create_engine('sqlite:///database.sqlite3')

# User.__table__.drop(engine)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def insert_user(user_id, secret_c):
    stmt_id_cafe = select(Cafe).where(Cafe.secret_code == secret_c)
    
    with engine.connect() as conn:
        res = conn.execute(stmt_id_cafe)
        cafe_id = res.first()[0]
        
        stmt = insert(User).values(telegram_id=user_id, cafe_id=cafe_id)
        conn.execute(stmt)
        conn.commit()


def is_user_in_table(user_id):
    stmt = select(User).where(User.telegram_id == user_id)
    
    with engine.connect() as conn:
        res = conn.execute(stmt)
        
        if res.first():
            return True
        else:
            return False

def get_cafe_by_user_id(user_id):
    stmt = select(User).where(User.telegram_id == user_id)
    
    with engine.connect() as conn:
        user_cafe_id = conn.execute(stmt).first()[2]
        stmt = select(Cafe).where(Cafe.id == user_cafe_id)
        cafe = conn.execute(stmt).first()
        return cafe[1]

