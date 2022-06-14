from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///invisman.db?check_same_thread=False', echo=True)
Base = declarative_base()

#Session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Session = sessionmaker(bind = engine)
#Base.metadata.create_all(engine)
