from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from .models import UserModel, UserDataModel, UserDataDetailModel
from .app import db

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='username cannot be blank', required=True)
    parser.add_argument('password', type=str, help='password cannot be blank', required=True)

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        
        current_user = UserModel.find_by_user_name(username)
        
        if not current_user:
            return {
                'message': 'username %s doesn\'t exist' % username
            }, 404

        if current_user.verify_password(password):
            access_token = create_access_token(identity=username)
            return {
                'access_token': access_token
            }
        else:
            return {
                'message': "invalid credentials"
            }, 401
