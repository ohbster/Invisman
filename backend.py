from database import Session, engine
from sqlalchemy import text, select, inspect

from flask import Flask
from flask import url_for
from flask import render_template
from models import *
import json
from multipledispatch import dispatch
from contextlib import contextmanager
#from app import get_session

session = Session()

#below is attempt to correct sqlalchemy pendingRollbackError that occurs when an
#attempt is made to update an object with in valid data. This error crashes the app
#thanks to user zvone @ https://stackoverflow.com/questions/52232979/sqlalchemy-rollback-when-exception

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise 
    else:
        session.commit()

Base.metadata.create_all(engine)
connection = engine.connect()

app = Flask(__name__)

class Model():
    #****************************
    #Common Functions
    #
    #****************************
    
    #snippet below inspired by:
    #user SuperShoot @ https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    
    #TODO: Rename this
    def row_as_dict(self, row):
        return {attribute.key: getattr(row, attribute.key)
                for attribute in inspect(row).mapper.column_attrs}
        
    def entity_properties(self, entity):
        return {str(attribute.key) : str(attribute.type)
                for attribute in inspect(entity).columns}

    def query_json(self, query=None):
        #for item in query(Store).all():
        if query is not None:
            data = {'data':[]}
            for row in query:
                data['data'].append(self.row_as_dict(row))
            return json.dumps(data)
        else:
            return None
    
    #@dispatch(Product)
    #this function was made redundant by set_entity    
    # def add_entity(self, new_entity=None):
    #     with get_session() as session:
    #         try:
    #             session.add(new_entity)
    #         except:
    #             session.rollback()
    #         else: 
    #             session.commit()
    
    def get_entity(self,model=None,entity_id=None):
        entity = session.query(model).get(entity_id)
        return self.row_as_dict(entity)
    
    def get_entities(self,model=None):
        result = self.query_json(session.query(model).all())
        if result is not None:
            return json.loads(result)
        # else:
        #     return {'body':[{
        #         'message': 'No results',
        #         'response': '200',
        #         }]}
    
    
    def get_entity_keys(self,model=None): 
        return [str(attribute.key)
        for attribute in inspect(model).columns]
        #This returned relationships as well. caused problems. 
        # keys = inspect(model).all_orm_descriptors.keys()
        # return keys
        
    def query(self, model=None, args=None, sort=None, direction=None):
        #TODO: This works, but looks sloppy. Try to clean this up
        keys = self.get_entity_keys(model)
        columns = inspect(model).mapper.columns
        query = session.query(model)
        for arg in args:
            if arg in keys: #equality 
                query = query.filter((columns[arg])==(args[arg]))
            elif arg == 'lt': #less than
                split_arg = args[arg].split(',')
                query = query.filter((columns[split_arg[0]])<(split_arg[1]))
            elif arg == 'gt': #greater than
                split_arg = args[arg].split(',')
                query = query.filter((columns[split_arg[0]])>(split_arg[1]))
            elif arg == 'le': #less than or equal
                split_arg = args[arg].split(',')
                query = query.filter((columns[split_arg[0]])<=(split_arg[1]))
            elif arg == 'ge': #greater than or equal
                split_arg = args[arg].split(',')
                query = query.filter((columns[split_arg[0]])>=(split_arg[1]))
        return json.loads(self.query_json(query))
    
    def set_entity(self,model=None,entity_id=None,attrs=None):
        with get_session() as session:
            try:
                #check if entity_id is None. if so, adding a new object
                if entity_id is None:
                    obj = model()
                else:
                #allowing a user to overwrite products by altering request
                    obj = session.query(model).get(entity_id) 
            
                #This mesthod is dangerous. Should not allow user to write the ID key.
                for c in inspect(obj).mapper.columns:
                    if c.key == 'id': #ignore id key as this is assigned by database, not form data
                        pass
                    elif str(c.type) == 'BOOLEAN':
                        if attrs[c.key] == 'True':
                            setattr(obj, c.key, True)
                        else:# c.key == 'False':
                            setattr(obj, c.key, False) 
                    else:
                        setattr(obj,c.key, attrs[c.key]) #assign the form data to the object's respective attribute
                       
                #check again if entity_id is None. If so, add the new object then commit
                if entity_id is None:
                    session.add(obj)
            except:
                session.rollback()
            else:
                #for an add this happens twice. avoid that
                session.commit()
                
    def search(self, model=None, column_list=None, substring=None):
        for column in column_list:
            query = session.query(model).column.contain(substring)
            result = query.all()
            return json.loads(result)
    #****************************
    #Product Functions
    #
    #****************************
    
    #Create
    
    @dispatch(Product)
    def add_product(self, new_product=None):
        self.add_entity(new_product)
    
    @dispatch(dict)
    def add_product(self, product_dict=None):
        self.set_entity(Product, None, product_dict)
    
    #Read
    
    #@dispatch(int)
    def get_product(self, product_id=None):
        return self.get_entity(Product,product_id)
    
    def get_products(self):
        return self.get_entities(Product)
        #return self.model.get_products()
    
    def get_product_keys(self):
        return self.get_entity_keys(Product)

    #Updates
 
    @dispatch(str,dict)
    def set_product(self, product_id=None, attrs=None): #attrs is json TODO: Need to pass product id into signature to avoid 
        return self.set_entity(Product,product_id,attrs)
     
    #delete 
     
    @dispatch(str)
    def delete_product(self, product_id):
        session.query(Product).filter_by(id=product_id).delete()
        session.commit()   
        
    def product_query(self, args=None, sort=None, direction=None):
        return self.query(Product,args,sort,direction)
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
    
    def get_store_keys(self):
        return self.get_entity_keys(Store)
    
    def store_query(self, args=None, sort=None, direction=None):
        return self.query(Store,args,sort,direction)
    #****************************
    #Inventory Functions
    #
    #****************************
    
    def add_inventory(self, inventory_dict):
        self.set_entity(Inventory, None, inventory_dict)
    
    def get_inventory(self, store_id):
        #return all inventory for store_id
        #Try to handle this by overloading get entities using a "filter" argument. I.e. "store_id=<store_id>"
        query = session.query(Inventory).filter_by(store_id=store_id)
        result = self.query_json(query)
        return json.loads(result)
    
    def get_inventories(self):
        return self.get_entities(Inventory)
    
    def get_inventory_keys(self):
        return self.get_entity_keys(Inventory)
    
    def get_unlisted_products(self, store_id):
        subquery1 = session.query(Inventory.product_id).filter_by(store_id=store_id).subquery()
        result = session.query(Product).filter(Product.id.in_(subquery1) )
        #result = session.query(Product.id).
        #Get all products where product_id is not in 
        ######(select all product_id from inventory where store_id = <store_id>)
        pass
    
    def get_listed_products(self, store_id):
        #This is reduntant: get_inventory(store_id) does this
        subquery1 = session.query(Inventory.product_id).filter_by(store_id=store_id).subquery()
        result = session.query(Product).filter(Product.id.in_(subquery1) )
        
        return result
    
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

    