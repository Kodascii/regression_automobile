from urllib.parse import urlsplit
from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from functools import wraps
from flask import abort
from app import app, db
from app.forms import LoginForm, RegistrationForm, PredictForm
from app.models import User
import requests
from currency_converter import CurrencyConverter



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
            'Brand': form.dropdown1.data,
            'Location': form.dropdown2.data,
            'Year': form.dropdown3.data,
            'Fuel_Type': form.dropdown4.data,
            'Transmission': form.dropdown5.data,
            'Owner_Type': form.dropdown6.data,
            'Kilometers_Driven': form.text_input1.data,
            'Mileage': form.text_input2.data,
            'Engine': form.text_input3.data,
            'Power': form.text_input4.data,
            'Seats': form.text_input5.data,
            'New_Price' : 0
        }
        session['form_data'] = form_data
        return redirect(url_for('result'))
    return render_template('predict.html', form=form)

def get_api_token():
    token_file = 'api_token.txt'
    try:
        with open(token_file, 'r') as file:
            token = file.read().strip()
        return token
    except FileNotFoundError:
        return None

@app.route('/result')
@login_required
def result():
    form_data = session.get('form_data', {})
    if not form_data:
        flash('No form data found.', 'error')
        return redirect(url_for('predict'))
    
    float_fields = ['Mileage', 'Engine', 'Power']
    int_fields = ['Year', 'Seats', 'Kilometers']

    # Convert the specified fields to floats
    for field in float_fields:
        if field in form_data and form_data[field] is not None:
            try:
                form_data[field] = float(form_data[field])
            except ValueError:
                flash(f"Invalid input for {field}, please enter a valid number.", 'error')
                return redirect(url_for('predict'))

    # Convert the specified fields to integers
    for field in int_fields:
        if field in form_data and form_data[field] is not None:
            try:
                form_data[field] = int(form_data[field])
            except ValueError:
                flash(f"Invalid input for {field}, please enter a whole number.", 'error')
                return redirect(url_for('predict'))

    # FastAPI endpoint URL
    token = get_api_token()
    if not token:
        flash('API token is required but was not found.', 'error')
        return redirect(url_for('predict'))

    fastapi_url = "http://localhost:8000/predict/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(fastapi_url, json=form_data, headers=headers)
        response.raise_for_status()
        prediction_result = response.json()
    except requests.exceptions.RequestException as e:
        flash(f"Error calling prediction API: {e}", 'error')
        return redirect(url_for('predict'))
    

    # convert from lakh to Indian Roupees to Euros
    cc = CurrencyConverter()
    lakh = 100000
    inr_value = prediction_result['prediction'][0] * lakh
    eur_value = round(cc.convert(inr_value, 'INR', 'EUR'), 2)
    prediction_result = eur_value

    return render_template('result.html', prediction=prediction_result, form_data=form_data)

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