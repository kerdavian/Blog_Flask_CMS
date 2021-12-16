from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, Required
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
  title = StringField('Title', validators=[Length(min=4, max=35), Required()])
  #   body = TextAreaField(
  #       'Body',
  #       validators=[
  #           Length(min=50,
  #                  max=4000,
  #                  message=
  #                  "Body length must be between %(min)d and %(max)d characters")
  #       ])
  teaser_image = FileField(
      'Teaser Image',
      render_kw={"accept": "image/*"},
      validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
  body = CKEditorField(
      'Body',
      validators=[
          Length(min=50,
                 max=4000,
                 message=
                 "Body length must be between %(min)d and %(max)d characters")
      ])
  submit = SubmitField(label=('Create'))