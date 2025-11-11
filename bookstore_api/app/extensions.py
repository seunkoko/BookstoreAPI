from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
