from database import engine_1
from models import User

User.metadata.create_all(bind=engine_1)

