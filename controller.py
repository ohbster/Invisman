
class Controller(object):
    def __init__(self,_model):
    #def __init__(self, _model, _view):
        self.model = _model
        #self.view = _view
    
    #****************************
    #Common Functions
    #
    #****************************
    def query(self, model=None, args=None, sort=None, direction='asc',paginate=False):
        return self.model.query(model, args, sort, direction, paginate)
    
    def query_json(self, query=None):
        return self.model.query_json(query)
    
    def row_as_dict(self, row=None):
        return self.model.row_as_dict(row)
    
    def entity_properties(self, entity=None):
        return self.model.entity_properties(entity)
    
    def get_entities(self,model=None):
        return self.model.get_entities(model)
    
    #****************************
    #Product Functions
    #
    #****************************      

    def add_product(self, product_dict=None):
        return self.model.add_product(product_dict)
      
    def get_product(self, product_id=None):
        return self.model.get_product(product_id)

    def get_products(self):
        return self.model.get_products()
    
    def get_product_keys(self):
        return self.model.get_product_keys()

    # def get_unlisted_products(self, store_id):
    #     return self.model.get_unlisted_products(store_id)
    
    def set_product(self, product_id=None, attrs=None):
        return self.model.set_product(product_id,attrs)
    
    def delete_product(self, product_id=None):
        return self.model.delete_product(product_id)
    
    def query_product(self,args=None, sort=None, direction=None, paginate=False):
        return self.model.query_product(args,sort,direction,paginate)
    
    def paginate(self, query=None,limit=None,page=1):
        return self.model.paginate(query,limit,page)
    #****************************
    #Store Functions
    #
    #****************************
        
    def get_store(self, store_id):
        store = self.model.get_store(store_id)
        return store
    
    def get_stores(self):
        return self.model.get_stores()
    
    def get_store_keys(self):
        return self.model.get_store_keys()
    
    def store_query(self,args=None, sort=None, direction=None):
        return self.model.store_query(args,sort,direction)
    
    #****************************
    #Quantity Functions
    #
    #****************************
    
    def add_quantity(self,product_id=None, store_id=None, quantity=None):
        return self.model.add_quantity(product_id, store_id, quantity)
    
    def get_quantities(self):
        return self.model.get_quantities()
    
    def get_quantity(self, product_id = None, store_id = None):
        return self.model.get_quantity(product_id, store_id)
        
    def set_quantity(self, product_id = None, store_id = None, quantity = None):
        self.model.set_quantity(product_id, store_id, quantity)
        
    #****************************
    #Inventory Functions
    #
    #****************************
    def add_inventory(self,inventory_dict=None):
        return self.model.add_inventory(inventory_dict)
        
    def get_inventory_keys(self):
        return self.model.get_inventory_keys()
    
    def get_inventory(self, store_id=None):
        return self.model.get_inventory(store_id)
    
    def get_inventories(self):
        return self.model.get_inventories()
    