from flask_sqlalchemy import SQLAlchemy
from typing import TYPE_CHECKING

db = SQLAlchemy()

# this is only needed for the flask-sqlalchemy stubs to work properly.
if TYPE_CHECKING:
  from flask_sqlalchemy.model import Model
  BaseModel = db.make_declarative_base(Model)
else:
  BaseModel = db.Model