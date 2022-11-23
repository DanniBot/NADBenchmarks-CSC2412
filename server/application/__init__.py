from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from application.config import Config
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required,  LoginManager
import boto3, botocore
import datetime


try: 
    from flask_restplus import Api, Resource
except ImportError:
    import werkzeug, flask.scaffold
    werkzeug.cached_property = werkzeug.utils.cached_property
    flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
    from flask_restplus import Api, Resource



api=Api()

app=Flask(__name__)
app.config.from_object(Config)

db=MongoEngine()
db.init_app(app)
# api.init_app(app)

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

### Dataset Model
class Dataset(db.Document):
    name = db.StringField(required=True, unique=True)  # name of the dataset
    slug = db.StringField( unique=True)  # slug field for url generation
    data_type = db.StringField(required=True)  # type of data  e.g. image, text, audio, video, numerical, etc.
    phases = db.StringField(required=True) # phases of the dataset  e.g. prevention, response, recovery, etc.
    description = db.StringField(required=True)  # description of the dataset
    image_url = db.StringField()  # image url for the dataset
    data_source = db.StringField(required=True)   # data source of the dataset
    size= db.StringField(required=True)      # size of the dataset
    timespan= db.StringField(required=True)   # timespan of the dataset
    geo_coverage= db.StringField(required=True)   # geographical coverage
    published= db.StringField(required=True)   # published date
    task_type = db.ListField(db.StringField()) # ML task type (regression, classification, segmentation, detection, etc.)
    topic = db.StringField(required=True)  # topic (natrual disaster, climate change, etc.)
    evaluated_on = db.ListField(db.StringField())  # evaluated on (e.g. COCO, VOC, etc.)
    metrics = db.ListField(db.StringField())  # metrics (e.g. accuracy, precision, recall, etc.)
    results = db.StringField(required=True) # MAE, RMSE, etc.
    paper_url = db.StringField(required=True)   # link to the source paper
    dataset_url = db.StringField()  # link to the dataset
    reference = db.StringField(required=True)   # reference
    approved = db.BooleanField(default=False)  # approval status
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Dataset, self).save(*args, **kwargs)


# Feedback Model
class Feedback(db.Document):
    first_name = db.StringField(required=True)  
    last_name = db.StringField() 
    email = db.StringField(required=True)  # email of the user
    subject = db.StringField()  # subject of the feedback
    message = db.StringField(required=True)  # message from the user
    timestamp = db.DateTimeField()  # timestamp of the feedback
    response = db.StringField()  # response from the admin
    replied = db.BooleanField(default=False)  # status of the feedback (replied or not)

    def save(self, *args, **kwargs):
        self.timestamp = datetime.datetime.now()
        super(Feedback, self).save(*args, **kwargs)



# Admin
class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Required for administrative interface
    def __unicode__(self):
        return self.login




# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()


# Create customized model view class
class MyModelView(ModelView):
    column_exclude_list = ['slug']
    column_searchable_list = ('name', 'description', 'reference','published')
    column_filters = ('name', 'topic', 'data_type', 'published','approved')


    def is_accessible(self):
        return current_user.is_authenticated
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login'))

class FeedbackView(MyModelView):
    column_list = ('timestamp','first_name', 'last_name', 'email', 'subject', 'message', 'response', 'Send Response')
    column_searchable_list = ['first_name', 'last_name', 'email', 'subject', 'message', 'response']
    column_filters = ['first_name', 'last_name', 'email', 'subject', 'message', 'response', 'timestamp']
    column_labels = dict(timestamp='Time', first_name='First Name', last_name='Last Name', email='Email', subject='Subject', message='Message', response='Response', Send_Response='Send Response')




init_login()
admin = Admin(app, name='NADBenchmarks', template_mode="bootstrap3")
admin.add_view(MyModelView(Dataset))
admin.add_view(FeedbackView(Feedback))

from application import routes




