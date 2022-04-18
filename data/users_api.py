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
    def get(self, user_id, json_type=True):
        user = abort_if_user_not_found(user_id)
        info = {'user': user.to_dict(only=('name', 'about', 'email', 'created_date')), 'user_favorites': user.get_favorites()}
        if json_type:
            return jsonify(info)
        return info

    # def delete(self, user_id):
    #     session = db_session.create_session()
    #     user = abort_if_user_not_found(user_id)
    #     if not user.is_admin:
    #         session.delete(user)
    #         session.commit()
    #         return jsonify({'success': 'OK'})
    #     return jsonify({'error': 'User is admin'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [user.to_dict(only=('name', 'about', 'email', 'created_date')) for user in users]})

    def post(self):
        try:
            args = parser_user_post.parse_args()
            session = db_session.create_session()
            user = User(
                name=args['name'],
                about=args['about'],
                email=args['email'],
                balance=args['balance'],
                hashed_password=set_password(args['password']))
            session.add(user)
            session.commit()
            return jsonify({'success': 'OK'})  # 'new_user': UsersResource.get(user_id=user.id, json_type=False)
        except:
            return jsonify({'error': 'wrong input data'})


parser_user_post = reqparse.RequestParser()
parser_user_post.add_argument('name', required=True)
parser_user_post.add_argument('about')
parser_user_post.add_argument('email', required=True)
parser_user_post.add_argument('balance', required=True, type=float)
parser_user_post.add_argument('password', required=True)
