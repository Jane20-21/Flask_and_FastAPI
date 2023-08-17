from flask import Flask, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm
from models import db, User
from flask_wtf.csrf import CSRFProtect
import secrets

secret_key = secrets.token_hex()
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
csrf = CSRFProtect(app)

with app.app_context():
    db.create_all()


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        h_password = generate_password_hash(password=password)
        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=h_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
        }
        return render_template('registered.html', **context)
    return render_template('register.html', form=form)
