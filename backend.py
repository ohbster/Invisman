from database import Session, engine
from sqlalchemy import text, select

from flask import Flask
from flask import url_for
from flask import render_template
from models import *
import json


session = Session()
Base.metadata.create_all(engine)
connection = engine.connect()

app = Flask(__name__)

class Model():
    
    def get_products(self):
        #return self.model.get_products()
        pass

    def get_unlisted_products(self, store_id):
        #return self.model.get_unlisted_products(store_id)
        pass
        
    def get_store(self, store_id):
        query = session.query(Store).filter_by(id=store_id)
        return json.dumps(query.scalar().__dict__)
        #store = self.model.get_store(store_id)
        #return store
       
    
    def get_stores(self):
        #return self.model.get_stores()
        pass
    
    def get_quantities(self):
        #return self.model.get_quantities()
        pass
    
    def get_quantity(self, product_id = None, store_id = None):
        #return self.model.get_quantity(product_id, store_id)
        pass

    def get_store_quantities(self, _store_id):
        #return self.model.get_store_quantities(_store_id)
        pass
    
    def get_product_quantities(self, _store_id):
        #return self.model.get_product_quantities(_store_id)
        pass
    
    def add_quantity(self,product_id=None, store_id=None, quantity=None):
        #return self.model.add_quantity(product_id, store_id, quantity)
        pass

    def add_product_quantity(self, _product_quantity = None):
        #self.model.add_product_quantity(_product_quantity)
        pass
        
    def set_quantity(self, product_id = None, store_id = None, quantity = None):
        #self.model.set_quantity(product_id, store_id, quantity)
        pass