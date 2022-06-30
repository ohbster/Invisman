from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///invisman.db?check_same_thread=False', echo=True)
Base = declarative_base()

Session = sessionmaker(bind = engine)

