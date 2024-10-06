from database import engine_1
from models_database import Base

Base.metadata.create_all(bind=engine_1)

