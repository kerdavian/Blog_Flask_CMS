from flask import Flask
from python_cms.db import db
from python_cms.blueprints.pages import pages_blueprint
from python_cms.blueprints.auth import auth_blueprint
from python_cms.models.user import UserModel
from python_cms.models.post import PostModel
from os import environ, path, mkdir
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
ROOT_PATH = app.root_path

# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# this will enable autoreload if the html files change
app.jinja_env.auto_reload = True
app.secret_key = environ.get('SECRET_KEY')

# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

#ez a kép feltöltéséhez kell
# https://flask-ckeditor.readthedocs.io/en/latest/index.html
app.config[
    'CKEDITOR_FILE_UPLOADER'] = 'pages.upload'  # this value can be endpoint or url
ckeditor = CKEditor(app)


@app.before_first_request
def create_tables():
  # create the files_upload folder if not exists. This is used by CKEditor images
  # and also the teaser image field when you create a blog post
  files_path = path.join(app.root_path, 'files_upload')
  if not path.exists(files_path):
    mkdir(files_path)
  # the app automatically creates the database tables before the first request, if
  # it does not exist
  db.create_all()


app.register_blueprint(pages_blueprint)
app.register_blueprint(auth_blueprint)


@login_manager.unauthorized_handler
def unauthorized():
  # This is what you get when you are not logged in but try to acccess a page
  # that can be only visited by authorized users. Could be changed to
  # a nice html template.
  return "You must be logged in to access this content.", 403


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
  return UserModel.get(user_id)


# this is only used in production. the flask run command ignores this.
# but when you deploy to heroku, this one will be used.
if __name__ == '__main__':
  # Threaded option to enable multiple instances for multiple user access
  # support
  app.run(threaded=True, port=80)