from flask import Flask, render_template, redirect, request, abort, url_for, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc, asc
from flask_restful import Api

from forms.game import FindForm, FilterForm
from forms.comment import CreateComment
from forms.user import RegisterForm, LoginForm, SettingsForm, AddBalanceForm

from data.comments import Comments
from data.games import Games
from data.users import User
from data import db_session, users_api, games_api
from pharse import *

import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret_key'
api = Api(app)

content_type = {1: 'Избранное', 2: 'Корзина', 3: 'Библиотека'}
responses = {'logout': Response(f'<a href="/register">Зарегестрируйтесь</a> или <a href="/login">войдите</a> в акаунт'),
             'private': Response(f'У вас нет доступа к этой странице <a href="/">Вернуться</a>')}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("store"))


@app.route("/index")
def index():
    return 'Рекламная страница'  # render_template("index.html")


@app.route("/")
def store():
    db_sess = db_session.create_session()
    start = request.args.get('start') if request.args.get('start') else 0
    count = request.args.get('count') if request.args.get('count') else 12
    if request.args.get('search') and current_user.is_authenticated and request.args.get('sort') in ['desk', 'ask']:
        try:
            sort_item = {'price': Games.discount_price, 'rating': Games.rating,
                         'date': Games.placement_date}[request.args.get('sort_by')]
            games = db_sess.query(Games).filter(Games.is_open | Games.id == current_user.id | current_user.is_admin,
                                                request.args.get('pstart') <= Games.discount_price,
                                                Games.discount_price <= request.args.get('pend')
                                                ).order_by(desc(sort_item) if request.args.get('sort') == 'desk' else
                                                           asc(sort_item), Games.id).offset(start).limit(count).all()
        except:
            return redirect(url_for("store"))
    else:
        if current_user.is_authenticated:
            games = db_sess.query(Games).filter(Games.is_open | Games.id == current_user.id | current_user.is_admin
                                                ).order_by(Games.id).offset(start).limit(count).all()
        else:
            games = db_sess.query(Games).filter(Games.is_open).order_by(Games.id).offset(start).limit(count).all()
    return render_template("store.html", games=games, title='RARE Games Store')


@app.route("/games/<int:id>/")
def games(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        game = db_sess.query(Games).filter(Games.id == id, (Games.is_open |
                                                            Games.user_id == current_user.id | current_user.is_admin)).first()
    else:
        game = db_sess.query(Games).filter(Games.id == id).first()
    comments = db_sess.query(Comments).filter(Comments.game_id == id).all()
    if game:
        return render_template("game.html", game=game, title=f'RARE {game.title}', comments=comments)
    return abort(404)


@app.route("/games/<int:id>/open/")
def games_open(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        game = db_sess.query(Games).filter(Games.id == id, (Games.user_id == current_user.id |
                                                            current_user.is_admin)).first()
        if game:
            game.show_all()
            db_sess.commit()
            return redirect(url_for("games", id=id))
    return abort(responses['private'])


@app.route("/games/<int:id>/delete/")
def games_delete(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        game = db_sess.query(Games).get(id)
        if game and (game.user_id == current_user.id or current_user.is_admin):
            db_sess.delete(game)
            db_sess.commit()
            return redirect(url_for("store"))
    return abort(responses['private'])


@app.route("/games/<int:id>/comment/", methods=['GET', 'POST'])
def comment(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        comment = db_sess.query(Comments).filter(Comments.game_id == id, Comments.user_id == current_user.id).first()
        if comment:
            form = CreateComment(rating=comment.rating, content=comment.content)
        else:
            form = CreateComment()

        if form.validate_on_submit():
            if not comment:
                comment = Comments(game_id=id, user_id=current_user.id,
                                   rating=form.rating.data,
                                   content=form.content.data)
                add_rating_to_game(game_id=id, rating=10 + form.rating.data)
                db_sess.add(comment)
            else:
                add_rating_to_game(game_id=id, rating=form.rating.data - comment.rating)
                comment.rating = form.rating.data
                comment.content = form.content.data
                comment.update_date()
            db_sess.commit()
            return redirect(url_for("games", id=id))
        return render_template("add_comment.html", title='Комментарий', form=form)
    return abort(responses['login'])


@app.route("/games/<int:id>/comment_delete/<int:comment_id>/")
def comment_delete(id, comment_id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        comment = db_sess.query(Comments).get(comment_id)
        if comment and (comment.user_id == current_user.id or current_user.is_admin) and comment.game_id == id:
            add_rating_to_game(game_id=id, rating=-10 - comment.rating)
            db_sess.delete(comment)
            db_sess.commit()
            return redirect(url_for("games", id=id))
        return abort(responses['private'])
    return abort(responses['login'])


@app.route("/profile/favorites/")
def favorites():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        games = db_sess.query(Games).filter(Games.id.in_(user.get_favorites())).all()
        return render_template("store_profile_content.html", content=content_type,
                               variant=1, games=games, title=content_type[1])
    return abort(responses['login'])


@app.route("/profile/basket/")
def basket():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        games = db_sess.query(Games).filter(Games.id.in_(user.get_basket())).all()
        args = {'price': sum([game.original_price for game in games]),
                'discount': sum([game.discount for game in games]),
                'total_price': sum([game.discount_price for game in games]),
                'mes': request.args.get('mes', '')}
        return render_template("store_profile_content.html", content=content_type,
                               variant=2, games=games, title=content_type[2], args=args)
    return abort(responses['login'])


@app.route("/profile/library/")
def library():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        games = db_sess.query(Games).filter(Games.id.in_(user.get_library())).all()
        return render_template("store_profile_content.html", content=content_type,
                               variant=3, games=games, title=content_type[3])
    return abort(responses['login'])


@app.route("/games/<int:id>/favorites/")
def set_favorites(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        if id not in user.get_favorites():
            user.add_favorites(id)
            add_rating_to_game(game_id=id, rating=10)
        else:
            user.del_favorites(id)
            add_rating_to_game(game_id=id, rating=-10)
        db_sess.commit()
    return redirect(url_for("games", id=id))


@app.route("/games/<int:id>/basket/")
def set_basket(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        if id not in user.get_basket():
            user.add_basket(id)
            add_rating_to_game(game_id=id, rating=15)
        else:
            user.del_basket(id)
            add_rating_to_game(game_id=id, rating=-15)
        db_sess.commit()
    return redirect(url_for("games", id=id))


@app.route("/buy_games/<int:user_id>/")
def set_library(user_id):
    if current_user.is_authenticated and user_id == current_user.id:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        games = db_sess.query(Games).filter(Games.id.in_(user.get_basket())).all()
        total_price = sum([game.discount_price for game in games])
        mes = 'Ошибка: Недостаточно средств!'
        if user.balance >= total_price:
            [user.add_library(game.id) for game in games]
            [user.del_basket(game.id) for game in games]
            [add_rating_to_game(game_id=game.id, rating=25) for game in games]
            user.balance -= total_price
            db_sess.commit()
            mes = 'Покупка совершена успешно!'
        return redirect(url_for("basket", mes=mes))
    return abort(responses['private'])


@app.route("/profile/", methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        return render_template("profile.html", title='Личный кабинет', user=user)
    return redirect(url_for("register"))


@app.route("/profile/settings/", methods=['GET', 'POST'])
def profile_settings():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        form = SettingsForm(name=user.name, about=user.about)
        if form.validate_on_submit():
            mes = "Неверный пароль"
            if user.check_password(form.old_password.data):
                user.name = form.name.data
                user.about = form.about.data
                if form.new_password.data and 5 <= len(form.new_password.data) <= 64 \
                        and form.new_password.data == form.new_password_again.data:
                    user.set_password(form.new_password.data)
                db_sess.commit()
                mes = "Новые данные сохранены"
            return render_template("profile_settings.html", title='Настройки профиля', form=form, message=mes)
        return render_template("profile_settings.html", title='Настройки профиля', form=form)
    return redirect(url_for("register"))


@app.route("/add_balance/", methods=['GET', 'POST'])
def add_balance():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        form = AddBalanceForm()
        if form.validate_on_submit():
            if user.check_password(form.password.data) and form.add_balance.data:
                user.add_balance(form.add_balance.data)
                db_sess.commit()
                return redirect(url_for("profile"))
            return render_template("add_balance.html", title='Пополнить баланс', user=user,
                                   form=form, message="Неверный пароль или сумма")
        return render_template("add_balance.html", title='Пополнить баланс', user=user, form=form)
    return redirect(url_for("register"))


@app.route("/add_game", methods=['GET', 'POST'])
def add_games():
    form = FindForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            count = form.result_count.data
            categories = [Categories[cat] for cat in Categories.keys() if cat in request.form]
            for game in game_find_similar(result_count=count, count=30 * form.select.data,
                                          keywords=form.keywords.data, categories=categories):
                if add_game(game, user_id=current_user.id):
                    count -= 1
                    if not count:
                        break
            return redirect(url_for("store"))
        return abort(responses['login'])
    return render_template("add_game.html", title='Добавление игры', form=form)


@app.route("/filter", methods=['GET', 'POST'])
def filter():
    form = FilterForm()
    if form.validate_on_submit():
        return redirect(url_for("store", search=1,
                                sort_by=['rating', 'price', 'date'][(form.data.get('select') - 1) // 2],
                                sort='desk' if form.data.get('select') % 2 == 1 else 'ask',
                                pstart=form.data.get('price_start'), pend=form.data.get('price_end'),
                                start=0, count=12))
    return render_template("filter.html", title='Поиск игр', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data,
                    email=form.email.data,
                    about=form.about.data)
        if form.password.data == app.config['SECRET_KEY']:  # admin
            user.is_admin = True
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("store"))
    return render_template("register.html", title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("store"))
        return render_template("login.html", message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


def add_rating_to_game(game_id, rating):
    db_sess = db_session.create_session()
    db_sess.query(Games).get(game_id).add_rating(rating)
    db_sess.commit()


def add_game(data, user_id=0):
    db_sess = db_session.create_session()
    if data:
        game = db_sess.query(Games).filter(Games.title == data['title']).first()
        if not game:
            game = Games()
            game.title = data['title']
            game.original_price = data['original_price']
            game.discount = data['discount']
            game.discount_price = data['discount_price']
            game.developer_name = data['developer_name']
            game.set_img_urls(data['image_urls'])
            game.set_published_date(data['published_date'])
            game.user_id = user_id
            db_sess.add(game)
        else:
            game.original_price = data['original_price']
            game.discount = data['discount']
            game.discount_price = data['discount_price']
        db_sess.commit()
        return True
    return False


def main():
    # db_session.global_init("db/store.db")
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db/store.db")
    db_session.global_init(db_path)

    api.add_resource(users_api.UsersListResource, '/api/v1/users')
    api.add_resource(users_api.UsersResource, '/api/v1/users/<int:user_id>')
    api.add_resource(games_api.GamesListResource, '/api/v1/games')
    api.add_resource(games_api.GamesResource, '/api/v1/games/<int:game_id>')

    # return app

    # db_sess = db_session.create_session()
    # for game in game_find_similar(start=0, count=50, keywords='',
    #                               categories=[Categories['CATEGORY_RACING']]):
    #     add_game(game, user_id=1)
    # db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()
    app.run(host='127.0.0.1', port=5000, debug=True)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
