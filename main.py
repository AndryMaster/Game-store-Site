from flask import Flask, render_template, redirect, request, abort, Response, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.game import FindForm
from forms.comment import CreateComment
from forms.user import RegisterForm, LoginForm

from data.comments import Comments
from data.games import Games
from data.users import User
from data import db_session
from pharse import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret_key'


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
    if current_user.is_authenticated:
        games = db_sess.query(Games).filter(Games.is_open | Games.id == current_user.id | current_user.is_admin).all()
    else:
        games = db_sess.query(Games).filter(Games.is_open).all()
    return render_template("index.html", games=games, title='RARE Games Store')


@app.route("/games/<int:id>/")
def games(id):
    print(url_for("games", id=id))
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        game = db_sess.query(Games).filter(Games.id == id, (Games.is_open |
                                           Games.user_id == current_user.id | current_user.is_admin)).first()
        comments = db_sess.query(Comments).filter(Comments.game_id == id).all()
        if game:
            return render_template("game.html", game=game, title=f'RARE: {game.title}', comments=comments,
                                   price={'op': value_to_str(game.original_price)})
    return abort(404)


@app.route("/games/<int:id>/open/")
def games_open(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        game = db_sess.query(Games).filter(Games.id == id, (Games.user_id == current_user.id |
                                                            current_user.is_admin)).first()
        if game:
            game.show_all()
            db_sess.commit()
            redirect(url_for("games", id=id))
    return abort(404)


@app.route("/games/<int:id>/delete/")
def games_delete(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        game = db_sess.query(Games).filter(Games.id == id, (Games.user_id == current_user.id |
                                                            current_user.is_admin)).first()
        if game:
            db_sess.delete(game)
            db_sess.commit()
            redirect(url_for("store"))
    return abort(404)


@app.route("/games/<int:id>/comment/")
def comment(id):
    form = CreateComment()
    if form.validate_on_submit() and current_user.is_authenticated:
        db_sess = db_session.create_session()
        if not db_sess.query(Comments).filter(Comments.game_id == id, Comments.user_id == current_user.id).first():
            comment = Comments(rating=form.rating.data, content=form.content.data)
            db_sess.add(comment)
            db_sess.commit()
        redirect(url_for("games", id=id))
    elif not current_user.is_authenticated:
        abort(404)
    return render_template('add_comment.html', title='Добавление комментария', form=form)


@app.route("/add_game")
def games_find():
    form = FindForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            for game in game_find_similar(result_count=form.result_count.data,
                                          start=0, count=50, keywords=form.keywords.data,
                                          categories=form.categories.data):
                add_game(game, user_id=current_user.id)
            db_sess.commit()
            redirect(url_for("store"))
        return abort(404)
    return render_template('add_game.html', title='Добавление игры', form=form)


# @app.route('/news', methods=['GET', 'POST'])
# @login_required
# def add_news():
#     form = NewsForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = News()
#         news.title = form.title.data
#         news.content = form.content.data
#         news.is_private = form.is_private.data
#         current_user.news.append(news)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect('/')
#     return render_template('news.html', title='Добавление новости', form=form)
#
#
# @app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#     if news:
#         db_sess.delete(news)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')
#
#
# @app.route('/news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     form = NewsForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#         if news:
#             form.title.data = news.title
#             form.content.data = news.content
#             form.is_private.data = news.is_private
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#         if news:
#             news.title = form.title.data
#             news.content = form.content.data
#             news.is_private = form.is_private.data
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     return render_template('news.html', title='Редактирование новости', form=form)
#
#
# @app.route("/")
# def index():
#     db_sess = db_session.create_session()
#     if current_user.is_authenticated:
#         news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
#     else:
#         news = db_sess.query(News).filter(News.is_private != True)
#     return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        user = User(name=form.name.data,
                    email=form.email.data,
                    about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        # return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


# def is_admin(id):
#     db_sess = db_session.create_session()
#     if db_sess.query(User).filter(User.id == id, User.is_admin).first().is_admin:
#         return 1
#     return 0


def add_game(data, user_id=0):
    db_sess = db_session.create_session()
    if data is not None:
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
        db_sess.commit()
        print(f"{game.__repr__()} was add to DB")


def main():
    db_session.global_init("db/store.db")
    app.run(host='127.0.0.1', port=8080, debug=True)

    # db_sess = db_session.create_session()
    # for game in game_find_similar(result_count=5,
    #                               start=0, count=50, keywords='',
    #                               categories=[Categories['CATEGORY_RACING']]):
    #     add_game(game, user_id=1)
    # db_sess.commit()

# error_response = Response("You do not have access rights to the page or it does not exist\n"
#                           "(У вас нет прав доступа к странице или её не существует)!")

if __name__ == '__main__':
    main()
