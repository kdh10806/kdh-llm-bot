from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, User, Purchase, Item

engine = create_engine("sqlite:///./test.db")
Session = sessionmaker(bind=engine)
session = Session()

#예제 데이터 추가
item1 = Item(name = "맥북13", price = 1000000, stock = 10, created_at=datetime.now())
item2 = Item(name = "맥북14", price = 1200000, stock = 10, created_at=datetime.now())
item3 = Item(name = "맥북15", price = 1400000, stock = 10, created_at=datetime.now())
item4 = Item(name = "삼성", price = 1200000, stock = 10, created_at=datetime.now())
item5 = Item(name = "엘지", price = 1100000, stock = 10, created_at=datetime.now())

session.add_all([item1, item2, item3, item4, item5])
session.commit()

user1 = User(name = "김대현", email = "kdh10806@gmail.com", phone = "01012341234", created_at = datetime.now())
user2 = User(name = "홍길동", email = "hkd123@gmail.com", phone = "01045674567", created_at = datetime.now())

session.add_all([user1, user2])
session.commit()

purchase1 = Purchase(user_id = user1.id, item_id = item1.id, quantity = 1, status = "paid", purchase_date = datetime.now())
purchase2 = Purchase(user_id = user2.id, item_id = item3.id, quantity = 1, status = "canceled", purchase_date = datetime.now())

session.add_all([purchase1, purchase2])
session.commit()