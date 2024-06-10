from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Person {self.name}>'
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_person_form')
def add_person_form():
    return render_template('add_person.html')

@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.form
    new_person = Person(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        occupation=data['occupation'],
        email=data['email'],
        phone=data['phone'],
        address=data['address']
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"message": "Person added sucessfully"}), 201

@app.route('/list_people_form')
def list_people_form():
    return render_template('list_people.html')

@app.route('/list_people', methods=['GET'])
def list_people():
    people = Person.query.all()
    results = [
        {
            "name": person.name,
            "age": person.name,
            "gender": person.gender,
            "occupation": person.occupation,
            "email": person.email,
            "phone": person.phone,
            "address": person.address,
        } for person in people]
    
    return jsonify(results), 200

@app.route('/search', methods=['GET'])
def search_people():
    query_params = request.args
    query = Person.query
    if 'age' in query_params:
        query = query.filter_by(age=query_params.get('age'))
    if 'gender' in query_params:
        query = query.filter_by(gender=query_params.get('gender'))
    if 'occupation' in query_params:
        query = query.filter_by(occupation=query_params.get('occupation'))
    if 'email' in query_params:
        query = query.filter_by(email=query_params.get('email'))
    if 'phone' in query_params:
        query = query.filter_by(phone=query_params.get('phone'))
    if 'address' in query_params:
        query = query.filter_by(address=query_params.get('address'))

    people = query.all()    
    results = [
        {
            "name": person.name,
            "age": person.name,
            "gender": person.gender,
            "occupation": person.occupation,
            "email": person.email,
            "phone": person.phone,
            "address": person.address,
        } for person in people]
    
    return jsonify(results), 200

@app.cli.command("create-db")
def create_db():
    with app.app_context():
        print('Creating DB')
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)