from flask import jsonify
from flask_restful import Resource, abort, reqparse
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user


def set_password(password):
    return generate_password_hash(password)


class UsersResource(Resource):
    def get(self, user_id):
        user = abort_if_user_not_found(user_id)
        return jsonify({'user': user.to_dict(only=('name', 'about', 'email', 'created_date',
                                                   'balance', 'hashed_password')),
                        'user_favorites': user.get_favorites()})

    def delete(self, user_id):
        session = db_session.create_session()
        user = abort_if_user_not_found(user_id)
        if not user.is_admin:
            session.delete(user)
            session.commit()
            return jsonify({'success': 'OK'})
        return jsonify({'error': 'User is admin'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(only=('name', 'about', 'email', 'created_date',
                                                     'balance', 'hashed_password')) for item in users]})

    def post(self):
        try:
            args = parser_user_post.parse_args()
            session = db_session.create_session()
            user = User(
                name=args['name'],
                about=args['about'],
                email=args['email'],
                balance=args['balance'],
                hashed_password=set_password(args['hashed_password']))
            session.add(user)
            session.commit()
            return jsonify({'success': 'OK'})
        except:
            return jsonify({'error': 'wrong input data'})


parser_user_post = reqparse.RequestParser()
parser_user_post.add_argument('name', required=True)
parser_user_post.add_argument('about')
parser_user_post.add_argument('email', required=True)
parser_user_post.add_argument('balance', required=True, type=float)
parser_user_post.add_argument('hashed_password', required=True)


# TEST

# from requests import get, post, delete
#
# print(get('http://localhost:5000/api/v2/users').json())
# print(get('http://localhost:5000/api/v2/users/5').json())
# print(get('http://localhost:5000/api/v2/users/52').json())
# print(get('http://localhost:5000/api/v2/users/q').json())
#
# print(post('http://localhost:5000/api/v2/users').json())
# print(post('http://localhost:5000/api/v2/users', json={'name': 'Sonya'}).json())
# print(post('http://localhost:5000/api/v2/users', json={'name': 'Sonya', 'position': 'junior programmer',
#                                                        'surname': 'Wolf', 'age': 17, 'address': 'module_3',
#                                                        'speciality': 'computer sciences',
#                                                        'hashed_password': 'wolf', 'email': 'wolf@mars.org'}).json())
#
# print(delete('http://localhost:5000/api/v2/users/999').json())
