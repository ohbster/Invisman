from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, ForeignKey 
from sqlalchemy import Date, Float
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__= 'products'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    image = Column(String, nullable = False) 
    description = Column(String(500)) 
    msrp = Column(Float, nullable = False)  
    
class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key = True, nullable = False) 
    type = Column(String(20), nullable = False) 
    address = Column(String(200), nullable = False) 
    
class Quantity(Base):
    __tablename__ = 'quantities'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key = True, nullable = False)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key = True, nullable = False)
    
    