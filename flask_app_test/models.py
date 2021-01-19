from .app import db
from .app import bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    user_name = db.Column(db.String())
    user_pwd = db.Column(db.String())
    is_active = db.Column(db.Boolean())
    created_time = db.Column(db.DateTime())

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.user_pwd, password)

    @classmethod
    def find_by_user_name(self, user_name):
        return self.query.filter_by(user_name=user_name).first()
