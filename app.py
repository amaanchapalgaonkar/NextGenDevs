from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/personalized_learning_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

app = Flask(__name__)

@app.route('/')
def home():
    return('index.html')

@app.route('/buy')
def buy():
    return('buy.html')

@app.route('/sell')
def sell():
    return('sell.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form['company_name']
        email = request.form['email']
        address = request.form['address']
        company_type = request.form['company_type']
        size = request.form['size']
        annual_emission = request.form['annual_emission']
        carbon_credits = request.form['carbon_credits']
        company_password = request.form['company_password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'warning')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Account created!', 'success')

    return render_template('register.html')

@app.route('/invest')
def invest():
    return('invest.html')

