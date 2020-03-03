from models.base_model import BaseModel
import peewee as pw
from flask_login import current_user
AWS_S3_DOMAIN = 'https://pleaseletmeusethisbucketname.s3-ap-southeast-1.amazonaws.com/'


class User(BaseModel):
    email = pw.CharField(unique=True)
    name = pw.CharField(unique=True)
    password = pw.CharField()
    image_path = pw.CharField(default = '')
    
    def profile_image_url(self):
        if str(self.image_path) == '':
            return AWS_S3_DOMAIN + 'empty.png'
        return AWS_S3_DOMAIN + self.image_path

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def validate(self):
        duplicate_name = User.get_or_none(User.name == self.name)
        duplicate_email = User.get_or_none(User.email == self.email)
        if current_user.is_authenticated:
            if current_user.name != self.name:
                if duplicate_name:
                    self.errors.append('Username not unique')
            if current_user.email != self.email:
                if duplicate_email:
                    self.errors.append('Email not unique')
        else:
            if duplicate_name:
                self.errors.append('Username not unique')
            if duplicate_email:
                self.errors.append('Email not unique')

