from flask import Flask, render_template, request
from blog.login_db import create_new_account, login, add_money

app = Flask(__name__)
app.secret_key = 'your_super_secret_random_key'


@app.route("/login", methods=["GET", "POST"])
def add_new_account():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        try:
            if login(name, password):
                print("Logged in")
                add_money(name, 10)
            else:
                create_new_account(name, password)
                print("Login failed")
        except:
            print("Error")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)