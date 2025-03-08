import pymysql
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/Hackathon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    company_type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    annual_emission = db.Column(db.Float, nullable=False)
    carbon_credits = db.Column(db.Float, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form['company_name']
        email = request.form['email']
        address = request.form['address']
        company_type = request.form['company_type']
        size = request.form['size']
        annual_emission = float(request.form['annual_emission'])
        carbon_credits = float(request.form['carbon_credits'])
        company_password = request.form['company_password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use another.', 'warning')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(company_password, method='pbkdf2:sha256')

        new_user = User(
            company_name=company_name,
            email=email,
            address=address,
            company_type=company_type,
            size=size,
            annual_emission=annual_emission,
            carbon_credits=carbon_credits,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account successfully created!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/invest')
def invest():
    return render_template('invest.html')

if __name__ == '__main__':
    app.run(debug=True)
