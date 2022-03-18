from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import desc, asc

from data import db_session
from data.games import Games


def abort_if_game_not_found(game_id):
    session = db_session.create_session()
    game = session.query(Games).get(game_id)
    if not game:
        abort(404, message=f"Game {game_id} not found")
    return game


class GamesResource(Resource):
    def get(self, game_id):
        game = abort_if_game_not_found(game_id)
        return jsonify({'games': {
            'game info': game.to_dict(only=('title', 'rating', 'placement_date', 'published_date',
                                       'developer_name', 'user_id', 'is_open')),
            'price': game.to_dict(only=('original_price', 'discount_price', 'discount')),
            'image_urls': game.get_img_urls()}})

    # def delete(self, game_id):
    #     session = db_session.create_session()
    #     game = abort_if_game_not_found(game_id)
    #     if not game.is_open:
    #         session.delete(game)
    #         session.commit()
    #     return jsonify({'success': 'OK'})


class GamesListResource(Resource):
    def get(self):
        args = parser_filter_games.parse_args()
        session = db_session.create_session()

        if args.get('search'):
            try:
                sort_item = {'price': Games.discount_price, 'rating': Games.rating,
                             'date': Games.placement_date}[args.get('sort_by')]
                games = session.query(Games).filter(Games.is_open,  args.get('price_start') <= Games.discount_price,
                                                    Games.discount_price <= args.get('price_end')
                                                    ).order_by(desc(sort_item) if args.get('sort') == 'desk' else
                                                               asc(sort_item), Games.id
                                                    ).offset(args.get('start')).limit(args.get('count')).all()
            except:
                return jsonify({'error': 'wrong input data'})
        else:
            games = session.query(Games).filter(Games.is_open).order_by(Games.id).all()

        return jsonify({'games': [{
            'game info': game.to_dict(only=('title', 'rating', 'placement_date', 'published_date',
                                            'developer_name', 'user_id', 'is_open')),
            'price': game.to_dict(only=('original_price', 'discount_price', 'discount')),
            'image_urls': game.get_img_urls()} for game in games]})

    # def post(self):
    #     args = parser_post_games.parse_args()
    #     session = db_session.create_session()
    #     game = session.query(Games).filter(Games.title == args['title']).first()
    #     if not game:
    #         try:
    #             game = Games(
    #                 title=args['title'],
    #                 original_price=args['original_price'],
    #                 discount=args['discount'],
    #                 discount_price=args['discount_price'],
    #                 developer_name=args['developer_name'],
    #                 user_id=1)
    #             game.set_img_urls(args['image_urls'])
    #             game.set_published_date(args['published_date'])
    #
    #             session.add(game)
    #             session.commit()
    #             return jsonify({'success': 'OK'})
    #         except:
    #             return jsonify({'error': 'wrong input data'})


parser_filter_games = reqparse.RequestParser()
parser_filter_games.add_argument('search', required=True, type=bool)
parser_filter_games.add_argument('sort_by', required=True)
parser_filter_games.add_argument('sort', required=True)
parser_filter_games.add_argument('price_start', required=True, type=int)
parser_filter_games.add_argument('price_end', required=True, type=int)
parser_filter_games.add_argument('is_finished', required=True, type=bool)
parser_filter_games.add_argument('start', required=True, type=int)
parser_filter_games.add_argument('count', required=True, type=int)

parser_post_games = reqparse.RequestParser()
parser_post_games.add_argument('title', required=True)
parser_post_games.add_argument('original_price', required=True, type=float)
parser_post_games.add_argument('discount', required=True, type=float)
parser_post_games.add_argument('discount_price', required=True, type=float)
parser_post_games.add_argument('developer_name', required=True)
parser_post_games.add_argument('image_urls', required=True, type=dict)
parser_post_games.add_argument('published_date', required=True)
