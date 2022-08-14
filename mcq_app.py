from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from my_forms import *
from functools import wraps


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def admin_required(func):
    def get_out(*args, **kwargs):
        flash("Vous devez être administrateur pour accéder à cette page", "danger")
        return redirect(url_for("log_in"))

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user or current_user.role != "admin":
            return get_out(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view


# app creation
app = Flask(__name__)

# login stuff
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'log_in'  # name of the login route function
login_manager.login_message = "Connexion requise pour accéder à la page."
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return UserDB.query.get(int(user_id))


# ORM
from my_ORM import *

# needed for forms & login
app.secret_key = "top cool"

""" DATABASE INIT 
________________________________________________________________________________________________________________________
"""
db.create_all()

if not UserDB.query.filter_by(user_name="UGLi").first():
    it_s_me = UserDB(user_name="UGLi", first_name="fred", last_name="leleu", email="ugli@mailo.com",
                     password="guigouguic",
                     role="admin")
    bidon = UserDB(user_name="bidon", first_name="bidon", last_name="BIDON", email="bidon@mailo.com",
                   password="bidon",
                   role="user")
    db.session.add(it_s_me)
    db.session.add(bidon)

    db.session.commit()

# q1 = QuestionDB(id=0,question="bla", answer1="truc", answer2="machin", correct=1)
# db.session.add(q1)
# db.session.commit()
""" 
________________________________________________________________________________________________________________________
"""


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['get', 'post'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserDB.query.filter_by(user_name=form.user_name.data).first()
        if not user or not user.password_match(form.password.data):
            flash(f"Nom d'utilisateur et/ou compte mail incorrects.", "danger")
            form.user_name.data = ""
        else:
            login_user(user, remember=form.remember.data)
            flash(f"Bienvenue {form.user_name.data} !", "success")
            # prevent open redirects
            next_ = request.args.get('next')
            if not is_safe_url(next_):
                return abort(400)
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


@app.route('/signup', methods=['get', 'post'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data != form.password_match.data:
            flash(f"Les mots de passe ne correspondent pas.", "danger")
        else:
            user_same_username = UserDB.query.filter_by(user_name=form.user_name.data).first()
            if user_same_username:
                flash(f"Le nom d'utilisateur {form.user_name.data} est déjà pris.", "danger")
                form.user_name.data = ''
            else:
                user_same_email = UserDB.query.filter_by(email=form.email.data).first()
                if user_same_email:
                    flash(f"L'adresse {form.email.data} est déjà utilisée", "danger")
                    form.email.data = ''
                else:
                    flash(f"Bienvenue {form.user_name.data}, ton compte a été créé.", "success")
                    user = UserDB(first_name=form.first_name.data,
                                  last_name=form.last_name.data,
                                  user_name=form.user_name.data,
                                  email=form.email.data,
                                  password=form.password.data)
                    db.session.add(user)
                    db.session.commit()
                    form.first_name.data = ''
                    form.last_name.data = ''
                    form.user_name.data = ''
                    form.email.data = ''
                    form.password = ''
                    form.password_match = ''
                    return redirect(url_for("log_in"))

    return render_template("signup.html", form=form)


@app.route('/logout')
@login_required
def log_out():
    name = current_user.user_name
    logout_user()
    flash(f"{name} est déconnecté.", "success")
    return redirect(url_for("index"))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route('/members')
@login_required
@admin_required
def members():
    users = UserDB.query.order_by(UserDB.date_added)
    return render_template("members.html", users=users)


@app.route('/updateuser/<name>')
@login_required
@admin_required
def update_user(name: str):
    user = UserDB.query.filter_by(user_name=name).first()
    if not user:
        flash("L'utilisateur n'existe pas", "danger")
        return redirect(url_for('members'))
    return render_template("updateuser.html", user=user)


@app.route('/delete/<name>')
@login_required
@admin_required
def delete_user(name):
    if current_user.user_name == name:
        flash("Impossible de supprimer votre propre compte.", "danger")
        return redirect(url_for('members'))
    else:
        UserDB.query.filter_by(user_name=name).delete()
        db.session.commit()
        flash("Utilisateur supprimé", "success")
        return redirect(url_for('members'))


@app.route('/changeuserrole/<name>')
@login_required
@admin_required
def change_user_role(name):
    user = UserDB.query.filter_by(user_name=name).first()
    user.role = "admin" if user.role == "user" else "user"
    db.session.commit()
    flash("Rôle de l'utilisateur modifié", "success")
    return redirect(url_for('members'))


@app.route('/groups')
@login_required
@admin_required
def groups():
    return render_template("groups.html")


# -------------- TEST
@app.route('/mcq')
def mcq():
    question = {"id": "00001",
                "statement_text": "Que fait le script suivant ?",
                "statement_code": """for i in range(5):
    print(i)""",
                "answers": [
                    {
                        "id": "4",
                        "text": "rien",
                        "code": ""
                    },
                    {
                        "id": "5",
                        "text": "tout",
                        "code": ""
                    },
                    {
                        "id": "6",
                        "text": "",
                        "code": "42"
                    }
                ],
                "solution": "4"
                }
    question2 = {"id": "00002",
                 "statement_text": "Qui est gogol ?",
                 "statement_code": "",
                 "answers": [
                     {
                         "id": "1",
                         "text": "rien",
                         "code": ""
                     },
                     {
                         "id": "2",
                         "text": "tout",
                         "code": ""
                     },
                     {
                         "id": "3",
                         "text": "",
                         "code": "42"
                     }
                 ],
                 "solution": 1
                 }
    quest = [question, question2]

    return render_template("mcq_test.html", quest=quest)


# -------------- END TEST
@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
