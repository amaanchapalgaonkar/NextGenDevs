import pymysql
from flask import Flask, request, render_template, url_for, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from ai_model import predict_emissions, predict_credits

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/Hackathon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class company_registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    company_type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    annual_emissions = db.Column(db.Float, nullable=False) 
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

        existing_user = company_registration.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use another.', 'warning')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(company_password, method='pbkdf2:sha256')

        new_user = company_registration(
    company_name=company_name,
    email=email,
    address=address,
    company_type=company_type,
    size=size,
    annual_emissions=annual_emission, 
    carbon_credits=carbon_credits,
    password=hashed_password )

        db.session.add(new_user)
        db.session.commit()

        flash('Account successfully created!', 'success')
        return redirect(url_for('home'))

    return render_template('registration.html')

@app.route('/invest')
def invest():
    return render_template('invest.html')

@app.route('/carbon')
def carbon():
    return render_template('carbon.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            required_fields = [
                'energy_usage', 'fuel_consumption', 
                'industrial_output', 'waste_generated', 
                'transport_distance'
            ]
            
            if not all(field in request.form for field in required_fields):
                return render_template('predict.html', error='Please fill in all fields.')
            
            input_data = [
                float(request.form['energy_usage']),
                float(request.form['fuel_consumption']),
                float(request.form['industrial_output']),
                float(request.form['waste_generated']),
                float(request.form['transport_distance'])
            ]

            predicted_emissions = predict_emissions(input_data)
            predicted_credits = predict_credits(input_data)

            return render_template('predict.html',
                                   emissions=predicted_emissions,
                                   credits=predicted_credits)
        except ValueError:
            return render_template('predict.html', error='Invalid input. Please enter valid numbers.')
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
