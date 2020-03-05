from models.base_model import BaseModel
import peewee as pw
from models.user import User


class FollowerFollowing(BaseModel):
    fan =  pw.ForeignKeyField(Image, backref='idols')
    idol =  pw.ForeignKeyField(Image, backref='fans')

    def validate(self):
        if fan == idol:
            self.errors.append("You can't follow yourself dummy!")