from database import Session, engine
from sqlalchemy import text, select, inspect

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
    
    #snippet below from:
    
    
    
    
    
    #user SuperShoot @ https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    def query_json(self, query=None):
        #query = session.query(Store)
        
        #for item in query(Store).all():
        if query is not None:
            data = {'data':[{}]}
            for row in query:
                data['data'].append(self.object_as_dict(row))
            return json.dumps(data)
        else:
            return None
    
    def get_products(self):
        #return self.model.get_products()
        pass

    def get_unlisted_products(self, store_id):
        #return self.model.get_unlisted_products(store_id)
        pass
        
    def get_store(self, store_id):
        query = session.query(Store).filter_by(id=store_id).scalar()
        data ={'data':[{
            
                'id': query.id,
                'type': query.type,
                'address': query.address,
                }],
            'response':'200',
            }
        data = json.dumps(data)
        
        return data
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