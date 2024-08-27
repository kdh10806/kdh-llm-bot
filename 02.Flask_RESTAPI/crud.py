from sqlalchemy.orm import Session
from models import Item
from datetime import datetime

def create_item(db: Session, name: str, price: int, stock: int):
    new_Item = Item(name=name, price=price, stock=stock, created_at=datetime.now())
    
    db.add(new_Item)
    db.commit()
    
    return new_Item

def get_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    
    return item

def get_all_items(db: Session):
    items = db.query(Item).all()
    
    return items

def update_item(db: Session, item_id: int, name: str=None, price: int=None, stock: int=None):
    item = get_item(db, item_id)
    
    if item is None:
        return None
    
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if stock is not None:
        item.stock = stock
        
    db.commit()
    
    return item
    
def delete_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    
    db.delete(item)
    db.commit()
    
    return item

