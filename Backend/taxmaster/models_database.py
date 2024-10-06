from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'Individual_User'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
