from flask import Flask, redirect, render_template, request, session, url_for
from forms import ArticleForm, LoginForm
from functools import wraps
from database import Database
import hashlib
import markdown

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "Lovecraftova kocka"

def login_required(func):
    @wraps(func)
    def foo(*args, **kwargs):
        if "logged" not in session:
            return redirect(url_for("view_login_form"))
        return func(*args, **kwargs)
    return foo


@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/articles")
def view_articles():
    articles = Database().get_articles()
    articles_html = []
    for article in articles:
        article = dict(article)
        article["content"] = markdown.markdown(article["content"])
        articles_html.append(article)
    return render_template("articles.jinja", articles=articles_html)

@app.route("/articles/<id>")
def get_article(id):
    article_by_id = Database().get_article_by_id(id)
    article = dict(article_by_id)
    article["content"] = markdown.markdown(article["content"])
    return render_template("article_by_id.jinja", article = article)


# admin routes

@app.route("/admin", methods=["GET", "POST"])
@login_required
def view_admin():
    article_form = ArticleForm()
    if request.method == "GET":
        return render_template("admin.jinja", form=article_form )
    else:
        title = article_form.title.data
        content = article_form.content.data
        Database().inser_article(title=title, content=content)
        return redirect(url_for("view_articles"))

@app.route("/admin/login", methods=["GET", "POST"])
def view_login_form():
    login_form = LoginForm()

    if request.method == "GET":
        return render_template("login.jinja", form=login_form)
    else:
        # admin: heslo
        db = Database()
        password_hash = hashlib.md5(login_form.password.data.encode()).hexdigest()

        user = db.validate_user(username=login_form.username.data, password=password_hash)
        #if login_form.username.data == "admin" and login_form.password.data == "heslo":
        if user:   
            session["logged"] = "username"
            return redirect(url_for("index"))
        else:
            return render_template("login.jinja", form=login_form)

@app.route("/admin/logout")
@login_required
def logout():
    session.pop("logged")
    return redirect(url_for("index"))




app.run()