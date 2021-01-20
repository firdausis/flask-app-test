from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.datastructures import FileStorage
import pandas as pd

from .models import UserModel, UserDataModel, UserDataDetailModel
from .app import db

class Login(Resource):
    """
    Resource for user authentication.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='username cannot be blank', required=True)
    parser.add_argument('password', type=str, help='password cannot be blank', required=True)

    def post(self):
        """
        Verify username and password to generate access token.
        """
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        
        current_user = UserModel.find_by_user_name(username)
        
        if not current_user:
            return {
                'message': 'username %s doesn\'t exist' % username
            }, 404

        if not current_user.is_active:
            return {
                'message': 'username %s is inactive' % username
            }, 401

        if current_user.verify_password(password):
            access_token = create_access_token(identity=username)
            return {
                'access_token': access_token
            }
        else:
            return {
                'message': "invalid credentials"
            }, 401

class DataFile(Resource):
    """
    Resource for dataset management.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')
    parser.add_argument('offset', type=int, location='args')
    parser.add_argument('limit', type=int, location='args')
    
    @jwt_required
    def post(self):
        """
        Send data file and create dataset entries.
        """
        current_username = get_jwt_identity()
        current_user = UserModel.find_by_user_name(current_username)

        args = self.parser.parse_args()
        file = args.get('file')
        if not file:
            return {
                'message': "file is not given"
            }, 400

        df = pd.read_excel(file.stream)
        total_count = len(df)

        userdata = UserDataModel(data_file_name=file.filename, total_count=total_count, user_id=current_user.id)
        userdata.save()

        success_count = 0
        for i,r in df.iterrows():
            data_year = r['Year']
            industry_aggregation_nzsioc = r['Industry_aggregation_NZSIOC']
            industry_code_nzsioc = r['Industry_code_NZSIOC']
            industry_name_nzsioc = r['Industry_name_NZSIOC']
            units = r['Units']
            variable_code = r['Variable_code']
            variable_name = r['Variable_name']
            variable_category = r['Variable_category']
            data_value = r['Value']
            industry_code_anzsic06 = r['Industry_code_ANZSIC06']
            
            userdatadetail = UserDataDetailModel(data_year=data_year, industry_aggregation_nzsioc=industry_aggregation_nzsioc,industry_code_nzsioc=industry_code_nzsioc, industry_name_nzsioc=industry_name_nzsioc, units=units, variable_code=variable_code, variable_name=variable_name, variable_category=variable_category, data_value=data_value, industry_code_anzsic06=industry_code_anzsic06, user_data_id=userdata.id)
            if userdatadetail.save():
                success_count += 1

        userdata.success_count = success_count
        userdata.fail_count = total_count - success_count
        userdata.save()
        
        return userdata.serialize(), 201

    @jwt_required
    def get(self):
        """
        List dataset metadata.
        """
        current_username = get_jwt_identity()
        current_user = UserModel.find_by_user_name(current_username)

        args = self.parser.parse_args()
        offset = args.get('offset')
        limit = args.get('limit')
        if not offset:
            offset = 0
        if not limit:
            limit = 10

        count = UserDataModel.count_by_user_id(current_user.id)
        userdata_list = UserDataModel.find_by_user_id(current_user.id, offset, limit)
        
        result = []
        for userdata in userdata_list:
            result.append(userdata.serialize())
        
        return {
            'count': count,
            'result': result,
        }

class DataFileDetail(Resource):
    """
    Resource for dataset management.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int, location='args')
    parser.add_argument('limit', type=int, location='args')

    @jwt_required
    def get(self, id):
        """
        View dataset details.
        """
        current_username = get_jwt_identity()
        current_user = UserModel.find_by_user_name(current_username)

        userdata = UserDataModel.find_by_id(id)
        if not userdata:
            return {
                'message': 'data file doesn\'t exist'
            }, 404
        if userdata.user_id != current_user.id:
            return {
                'message': 'user is unauthorized'
            }, 401

        args = self.parser.parse_args()
        offset = args.get('offset')
        limit = args.get('limit')
        if not offset:
            offset = 0
        if not limit:
            limit = 10

        count = UserDataDetailModel.count_by_user_data_id(id)
        userdatadetail_list = UserDataDetailModel.find_by_user_data_id(id, offset, limit)
        
        result = []
        for userdatadetail in userdatadetail_list:
            result.append(userdatadetail.serialize())
        
        return {
            'count': count,
            'result': result,
        }
