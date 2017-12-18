from flask_restful import Resource, reqparse
from models.user import UserModel

#/usr/bin/newman -> /usr/lib/node_modules/newman/bin/newman.js


class UserRegister(Resource):
    """
    this resource allows users to register by sending a
    POST request with their username and password
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='this field cannot be blank.')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exist'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created OK'}, 201

class User(Resource):
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': 'user deleted'}
        return {'message': 'no such user'}, 404

class UserList(Resource):
    def get(self):
        return {'users': [x.json() for x in UserModel.query.all()]}