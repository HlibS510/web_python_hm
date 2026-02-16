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


@app.route("/register", methods=["GET", "POST"])
def register():
    session["loggined"] = False
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        if session["loggined"] == False:
            try:
                if login(name, password):
                    print("Logged in")
                    session["login_name"] = name
                    session["loggined"] = True
                    return redirect(url_for("index"))
                else:
                    create_new_account(name, password)
                    print("Login failed")
                    session["login_name"] = name
                    session["loggined"] = True
                    return redirect(url_for("index"))
            except:
                print("Error")
        else:
            print("logged in")
    return render_template("login.html")

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

    if request.method == "POST":
        name = session["login_name"]
        text = request.form["text"]
        image = request.form["image"]
        section_id = int(request.form["section"])
        create_new_post(name, text, image, section_id)
        section = get_section_by_id(section_id)
        return redirect(url_for("section_page", sections=sections, section_slug=section["slug"]))

    return render_template("add_post.html", sections=sections, name=display_name)

app.run()
