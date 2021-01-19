import datetime
from sqlalchemy.exc import SQLAlchemyError

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

class UserDataModel(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, primary_key=True)
    data_file_name = db.Column(db.String())
    total_count = db.Column(db.Integer(), default=0)
    success_count = db.Column(db.Integer(), default=0)
    fail_count = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer())
    created_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    def serialize(self):
        return {
            'id': self.id,
            'data_file_name': self.data_file_name,
            'total_count': self.total_count,
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def count_by_user_id(self, user_id):
        return self.query.filter_by(user_id=user_id).count()

    @classmethod
    def find_by_user_id(self, user_id, offset, limit):
        return self.query.filter_by(user_id=user_id).order_by(UserDataModel.created_time.desc()).offset(offset).limit(limit)

    @classmethod
    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

class UserDataDetailModel(db.Model):
    __tablename__ = 'user_data_details'

    id = db.Column(db.Integer, primary_key=True)
    data_year = db.Column(db.Integer())
    industry_aggregation_nzsioc = db.Column(db.String())
    industry_code_nzsioc = db.Column(db.String())
    industry_name_nzsioc = db.Column(db.String())
    units = db.Column(db.String())
    variable_code = db.Column(db.String())
    variable_name = db.Column(db.String())
    variable_category = db.Column(db.String())
    data_value = db.Column(db.Integer())
    industry_code_anzsic06 = db.Column(db.String())
    user_data_id = db.Column(db.Integer())
    created_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    def serialize(self):
        return {
            'id': self.id,
            'data_year': self.data_year,
            'industry_aggregation_nzsioc': self.industry_aggregation_nzsioc,
            'industry_code_nzsioc': self.industry_code_nzsioc,
            'industry_name_nzsioc': self.industry_name_nzsioc,
            'units': self.units,
            'variable_code': self.variable_code,
            'variable_name': self.variable_name,
            'variable_category': self.variable_category,
            'data_value': self.data_value,
            'industry_code_anzsic06': self.industry_code_anzsic06,
            'user_data_id': self.user_data_id,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def count_by_user_data_id(self, user_data_id):
        return self.query.filter_by(user_data_id=user_data_id).count()

    @classmethod
    def find_by_user_data_id(self, user_data_id, offset, limit):
        return self.query.filter_by(user_data_id=user_data_id).offset(offset).limit(limit)
