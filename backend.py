from database import Session, engine
from sqlalchemy import text, select, inspect, not_

from flask import Flask
from flask import url_for
from flask import render_template
from models import *
import json
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
        
    def query(self, model=None, args=None, sort=None, direction=None, paginate=False):
        #TODO: This works, but looks sloppy. Try to clean this up
        keys = self.get_entity_keys(model)
        columns = inspect(model).mapper.columns
        query = session.query(model)
        if args is not None:
            for arg in args:
                if arg in keys: #equality 
                    query = query.filter((columns[arg])==(args[arg]))
                elif arg == 'lt': #less than
                    split_arg = args[arg].split(',') #seperate "key,value" into "key", "value"
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
        #sorting
        if sort is not None: #check if sort is a valid key
            if direction == 'asc':
                query = query.order_by(columns[sort].asc())
            elif direction == 'desc':
                query = query.order_by(columns[sort].desc())
        #to paginate or not
        #this bool is used to return raw query in order to paginate with limit
        #and offset supplied by flask
        
        if paginate is True: 
            result = {'query':query, 
                     'count':query.count()}
            #return query
            return result
        #if paginate is set to false, just return the query as json
        else:
            return json.loads(self.query_json(query))
    
    
        
    def paginate(self, query, limit=None, page=None):
        offset = (page - 1)* limit
        query = query.limit(limit).offset(offset)
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
    
    def product_properties(self):
        return self.entity_properties(Product)

    #Updates
 
    def set_product(self, product_id=None, attrs=None): #attrs is json TODO: Need to pass product id into signature to avoid 
        return self.set_entity(Product,product_id,attrs)
     
    #delete 
     
    def delete_product(self, product_id):
        session.query(Product).filter_by(id=product_id).delete()
        session.commit()   
        
    def query_product(self, args=None, sort=None, direction=None, paginate=True):
        return self.query(Product,args,sort,direction,paginate)
    
    def product_query_page_data(self,):
        pass
    #****************************
    #Store Functions
    #
    #****************************
    def add_store(self, store_dict=None):
        self.set_entity(Store, None, store_dict)
    
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
    
    def query_store(self, args=None, sort=None, direction=None, paginate=True):
        return self.query(Store,args,sort,direction,paginate)
    
    def get_stores(self):
        #return self.model.get_stores()
        pass
    
    def get_store_keys(self):
        return self.get_entity_keys(Store)
    
    def store_properties(self):
        return self.entity_properties(Store)
    #****************************
    #Inventory Functions
    #
    #****************************
    
    def add_inventory(self, inventory_dict):
        self.set_entity(Inventory, None, inventory_dict)
        
    def multiadd_inventory(self, store_id=None, product_ids=None):
        #TODO: Rewrite. This does not account for changes to inventory schema
        for product in product_ids['data']: 
            self.add_inventory({
            'store_id':store_id,
            'quantity':0,
            'active':False,
            'product_id':product['id']
            })
            
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
        result = session.query(Product).filter(Product.id.not_in(subquery1) )
        
        return json.loads(self.query_json(result))
        #result = session.query(Product.id).
        #Get all products where product_id is not in 
        ######(select all product_id from inventory where store_id = <store_id>)
    
    def get_listed_products(self, store_id):
        #This is reduntant: get_inventory(store_id) does this
        listed = session.query(Inventory.product_id).filter_by(store_id=store_id).subquery()
        result = session.query(Product).filter(Product.id.in_(listed) )
    
        return json.loads(self.query_json(result))
    

    