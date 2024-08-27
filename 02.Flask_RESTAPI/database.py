#python -> DB connection(SQLAlchemy)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
#Autocommit = db.commit() 데이터 변형
#Autoflush = db에 데이터를 보내는 것 작업을 효율적으로 관리할 수 있게 된다.

def init_db():
    Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    except:
        db.close()