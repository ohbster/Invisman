from database import Session, engine
from sqlalchemy import text, select, inspect

from flask import Flask
from flask import url_for
from flask import render_template
from models import *
import json
from multipledispatch import dispatch

session = Session()
Base.metadata.create_all(engine)
connection = engine.connect()

app = Flask(__name__)

class Model():
    
    #****************************
    #Common Functions
    #
    #****************************
    
    #snippet below from:
    #user SuperShoot @ https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    def query_json(self, query=None):
        #for item in query(Store).all():
        if query is not None:
            data = {'data':[]}
            for row in query:
                data['data'].append(self.object_as_dict(row))
            return json.dumps(data)
        else:
            return None
    
    #****************************
    #Product Functions
    #
    #****************************
    
    #Create
    
    @dispatch(Product)
    def add_product(self, product_new=None):
        session.add(product_new)
        session.commit()
    
    @dispatch(dict)
    def add_product(self, product_dict=None):
        obj = Product()
        for c in inspect(obj).mapper.column_attrs:
            if c.key != 'id': #ignore id key as this is assigned by database, not form data
                setattr(obj,c.key, product_dict[c.key]) #assign the form data to the object's respective attribute
        self.add_product(obj)
    
    #Read
    
    #@dispatch(int)
    def get_product(self, product_id=None):
        product = session.query(Product).get(product_id)
        return self.object_as_dict(product)
    
    def get_products(self):
        #return self.model.get_products()
        pass
    
    def get_product_keys(self):
        keys = inspect(Product).all_orm_descriptors.keys()
        return keys

    def get_unlisted_products(self, store_id):
        #return self.model.get_unlisted_products(store_id)
        pass
    
    #Updates
 
    @dispatch(str,dict)
    def set_product(self, product_id=None, attrs=None): #attrs is json TODO: Need to pass product id into signature to avoid 
        #allowing a user to overwrite products by altering request
        obj = session.query(Product).get(product_id) 
        
        #This mesthod is dangerous. Should not allow user to write the ID key.
        for key in attrs: #for each attribute in the attrs list, assign its value to the product_new
            if key != 'id': #skip id!
                setattr(obj, key, attrs[key])
        session.commit()
     
    #delete 
     
    @dispatch(str)
    def delete_product(self, product_id):
        session.query(Product).filter_by(id=product_id).delete()
        session.commit()   
        
    #****************************
    #Store Functions
    #
    #****************************
    
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
    
    def get_stores(self):
        #return self.model.get_stores()
        pass
    
    #****************************
    #Quantity Functions
    #
    #****************************
    
    # def add_quantity(self,product_id=None, store_id=None, quantity=None):
    #     #return self.model.add_quantity(product_id, store_id, quantity)
    #     pass
    #
    # def get_quantities(self):
    #     #return self.model.get_quantities()
    #     pass
    #
    # def get_quantity(self, product_id = None, store_id = None):
    #     #return self.model.get_quantity(product_id, store_id)
    #     pass

    #****************************
    #Relationship Functions
    #
    #****************************
    
    # def get_store_quantities(self, _store_id):
    #     #return self.model.get_store_quantities(_store_id)
    #     pass
    #
    # def get_product_quantities(self, _store_id):
    #     #return self.model.get_product_quantities(_store_id)
    #     pass
    #
    # def add_product_quantity(self, _product_quantity = None):
    #     #self.model.add_product_quantity(_product_quantity)
    #     pass
    #
    # def set_quantity(self, product_id = None, store_id = None, quantity = None):
    #     #self.model.set_quantity(product_id, store_id, quantity)
    #     pass
    #

    