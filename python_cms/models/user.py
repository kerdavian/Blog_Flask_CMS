from python_cms.db import BaseModel, db
from flask_login import UserMixin


class UserModel(BaseModel, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.String(80), primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False, unique=True)
  profile_pic = db.Column(db.String(80))
  # one user can have multiple posts (many to one relationship)
  posts = db.relationship('PostModel', back_populates='author')

  def __init__(self, id, name, email, picture):
    self.id = id
    self.name = name
    self.email = email
    self.profile_pic = picture

  @classmethod
  def get(cls, user_id):
    return cls.query.filter_by(id=user_id).first()

  def save(self):
    db.session.add(self)
    db.session.commit()