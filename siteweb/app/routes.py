from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from functools import wraps
from flask import abort
from app import app, db
from app.forms import LoginForm, RegistrationForm, PredictForm
from app.models import User



def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.isAdmin:
            abort(403)  # Return a 403 Forbidden error if the user is not an admin
        return func(*args, **kwargs)
    return decorated_view


@app.route('/')
@app.route('/accueil')
def accueil():   
    return render_template('index.html', title='Accueil')


@app.route('/stats')
@login_required
@admin_required
def stats():   
    return render_template('stats.html', title='Statistics')

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictForm()
    if form.validate_on_submit():
        form_data = {
            'Name': form.dropdown1.data,
            'Location': form.dropdown2.data,
            'Year': form.dropdown3.data,
            'Fuel Type': form.dropdown4.data,
            'Transmission': form.dropdown5.data,
            'Owner Type': form.dropdown6.data,
            'Kilometers': form.text_input1.data,
            'Mileage': form.text_input2.data,
            'Engine': form.text_input3.data,
            'Power': form.text_input4.data,
            'Seats': form.text_input5.data
        }
        session['form_data'] = form_data
        return redirect(url_for('result'))
    return render_template('predict.html', form=form)


@app.route('/result')
@login_required
def result():
    form_data = session.get('form_data', {})  # Retrieve form data from session
    if not form_data:
        flash('No form data found.', 'error')
        return redirect(url_for('predict'))
    
    return render_template('result.html', form_data=form_data)

@app.route('/joke')
@login_required
def joke():   
    return render_template('joke.html', title='Joke')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accueil'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('accueil')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('accueil'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('accueil'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

from .plot_generator import init_plot
init_plot()