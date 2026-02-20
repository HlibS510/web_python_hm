from flask import Flask, render_template, request, redirect, url_for, session
from db import *
from login_db import *

app = Flask(__name__)
app.secret_key = 'egtrxcsaaadfrjikloptr'

@app.route('/', methods=["GET", "POST"])
def index():
    display_name = session.get("login_name", "Login")
    sections = get_blog_sections()
    results = None
    input = None

    if request.method == "POST":
        input = request.form.get("input")
        results = find_post(input)

    return render_template('index.html', sections=sections, results=results, input=input, name=display_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    session["login"] = False
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        if login_user(name, password):
            print("Logged in")
            session["login_name"] = name
            session["login"] = True
            return redirect(url_for("index"))
        else:
            error = 'Incorrect password or username.'
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    session["login"] = False
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        if create_new_account(name, password):
            session["login_name"] = name
            session["login"] = True
            return redirect(url_for("index"))
        else:
            error = 'Username is already used, or something went wrong'

    return render_template("register.html")

@app.route('/<section_slug>')
def section_page(section_slug):
    display_name = session.get("login_name", "Login")
    sections = get_blog_sections()
    section = get_section_by_slug(section_slug)

    if not section:
        return "404 Not Found", 404

    posts = get_section_posts(section["id"])

    return render_template('section.html',sections=sections , section=section, posts=posts, name=display_name)


@app.route('/like/<post_id>')
def like_post(post_id):
    like(post_id)

    return redirect(request.referrer)

@app.route("/add", methods=["GET", "POST"])
def add_post():
    display_name = session.get("login_name", "Login")
    sections = get_blog_sections()
    login_name = session.get("login_name")

    if login_name:
        if request.method == "POST":
            name = session["login_name"]
            text = request.form["text"]
            image = request.form["image"]
            section_id = int(request.form["section"])
            create_new_post(name, text, image, section_id)
            section = get_section_by_id(section_id)
            return redirect(url_for("section_page", sections=sections, section_slug=section["slug"]))
    else:
        return redirect(url_for("register"))

    return render_template("add_post.html", sections=sections, name=display_name)

app.run()
