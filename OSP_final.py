from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    level = db.Column(db.String(10))  # level 컬럼 추가
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    goal = db.Column(db.String(50))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods=['POST'])
def add_user():
    data = request.form
    if not data or 'email' not in data:
        return "Email is required", 400

    # Check if user already exists
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return "User already exists", 200

    # Create a new user
    user = User(
        email=data['email'], 
        name=data.get('name'), 
        level=data.get('level')
    )
    db.session.add(user)
    db.session.commit()

    # Redirect based on the 'level' value
    if user.level == '초급':
        return redirect(url_for('beginner'))
    elif user.level == '중급':
        return redirect(url_for('intermediate'))
    elif user.level == '고급':
        return redirect(url_for('advanced'))

    return redirect(url_for('index'))

@app.route('/beginner')
def beginner():
    return render_template('beginner.html')  # 초급 HTML 파일을 렌더링

@app.route('/intermediate')
def intermediate():
    return render_template('intermediate.html')  # 중급 HTML 파일을 렌더링

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')  # 고급 HTML 파일을 렌더링

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()

# Call the function to create tables when the app starts
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
