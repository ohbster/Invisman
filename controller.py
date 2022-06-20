

class Controller(object):
    def __init__(self, _model, _view):
        self.model = _model
        self.view = _view
    
    def draw_inventory(self): #check this one
        products = self.model.get_product()
        self.view.draw_inventory()
        
    def show_product(self, _product_id): #check this one
        item = self.model.get_item(_product_id)
        self.view.draw_inventory()

    def get_products(self):
        return self.model.get_products()

    def get_unlisted_products(self, store_id):
        return self.model.get_unlisted_products(store_id)
        
    def get_store(self, store_id):
        store = self.model.get_store(store_id)
        return store
    
    def get_stores(self):
        return self.model.get_stores()
    
    def get_quantities(self):
        return self.model.get_quantities()
    
    def get_quantity(self, product_id = None, store_id = None):
        return self.model.get_quantity(product_id, store_id)

    def get_store_quantities(self, _store_id):
        return self.model.get_store_quantities(_store_id)
    
    def get_product_quantities(self, _store_id):
        return self.model.get_product_quantities(_store_id)
    
    def add_quantity(self,product_id=None, store_id=None, quantity=None):
        return self.model.add_quantity(product_id, store_id, quantity)

    def add_product_quantity(self, _product_quantity = None):
        self.model.add_product_quantity(_product_quantity)
        
    def set_quantity(self, product_id = None, store_id = None, quantity = None):
        self.model.set_quantity(product_id, store_id, quantity)
        
    def query_json(self):
        return self.model.query_json()
    #********
    #Testing below
    #********
    def query_json2(self, query=None):
        return self.model.query_json2(query=None)
    
    def query_json3(self, query=None):
        return self.model.query_json3(query=None)