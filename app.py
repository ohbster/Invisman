from flask import Flask
from flask import url_for
from flask import render_template
from database import Session, engine
from sqlalchemy import text, select
from controller import Controller
from models import *
from backend import Model
import json


#dummy view class
class View():
    def __init__(self):      
        self.controller = None
        
    def set_controller(self, controller=None):
        self.controller = controller
    
    def get_controller(self):
        return self.controller
        
    def dummy(self):
        pass
    
model = Model()
view = View()
app_controller = Controller(_model=model, _view=view)
view.set_controller(app_controller)

session = Session()
Base.metadata.create_all(engine)
connection = engine.connect()


app = Flask(__name__)