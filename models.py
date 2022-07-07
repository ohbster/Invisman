from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, ForeignKey 
from sqlalchemy import Date, Float
from sqlalchemy.orm import relationship
from database import Base

from database import Session, engine
Base.metadata.create_all(engine)
connection = engine.connect()

class Product(Base):
    __tablename__= 'products'
    id = Column(Integer, primary_key = True, nullable = False)
    sku = Column(String, unique = True)
    name = Column(String, nullable = False)
    image = Column(String, nullable = False) 
    description = Column(String(500)) 
    msrp = Column(Float, nullable = False)  
    #active = Column(Boolean, nullable = False)
    inventory = relationship('Inventory', backref='product', lazy=True)
    
class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key = True, nullable = False) 
    name = Column(String, nullable = False)
    website = Column(String(20), nullable = False) 
    address = Column(String(200), nullable = False) 
    
    inventory = relationship('Inventory', backref='store', lazy=True)
    
class Inventory(Base):
    __tablename__ = 'inventories'
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key = True, nullable = False)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key = True, nullable = False)
    quantity = Column(Integer, nullable = False)
    active = Column(Boolean, nullable = False)
    
    