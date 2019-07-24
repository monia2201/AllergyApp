from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request
from datetime import datetime
import statistics

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'   #tylko bieżące wyniki, nie zapisywane w bazie
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)


class Formdata(db.Model):
    __tablename__ = 'database__'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    eyes = db.Column(db.String)
    sex = db.Column(db.String)
    q1 = db.Column(db.String)
    q2 = db.Column(db.String)
    q3 = db.Column(db.String)
    q4 = db.Column(db.String)
    q5 = db.Column(db.String)
    q6 = db.Column(db.String)
    q7 = db.Column(db.String)
    q8 = db.Column(db.String)
    q9 = db.Column(db.String)


def __init__(self, id, firstname, email, sex, age, eyes, q1, q2, q3, q4, q5, q6, q7, q8, q9):
    self.id = id
    self.firstname = firstname
    self.email = email
    self.age = age
    self.eyes = eyes.lower()
    self.sex = sex
    self.q1 = q1
    self.q2 = q2
    self.q3 = q3
    self.q4 = q4
    self.q5 = q5
    self.q6 = q6
    self.q7 = q7
    self.q8 = q8
    self.q9 = q9


db.create_all()


def probability_for_one():
    prob = []
    tupla=()
    personality = db.session.query(Formdata).all()
    for i in personality:
        if i.q4 == "Nie":
            pers_prob = 64
            prob.append(64)
            name = "umiarkowane"
            color = "yellow"
        elif i.q4 == "Tak" and i.q8 == "Nie":
            pers_prob = 83
            prob.append(83)
            name = "średnie"
            color = "orange"
        elif i.q4 == "Tak" and i.q6 == "Nie" and i.q8 == "Tak":
            pers_prob = 97
            prob.append(97)
            name = "wysokie"
            color = "red"
        elif i.q1 == "Nie" and i.q4 == "Tak" and i.q6 == "Tak" and i.q8 == "Tak":
            pers_prob = 95
            prob.append(95)
            name = "wysokie"
            color = "red"
        elif i.q1 == "Tak" and i.q4 == "Tak" and i.q6 == "Tak" and i.q8 == "Tak":
            pers_prob = 80
            prob.append(80)
            name = "średnie"
            color = "orange"
        else:
            pers_prob = 20
            prob.append(20)
            name = "niskie"
            color = "green"

        mean_prob = statistics.mean(prob)
        if mean_prob > 0 and mean_prob <50:
            color2="green"
        if mean_prob >=50 and mean_prob <80:
            color2="yellow"
        if mean_prob >=80 and mean_prob <90:
            color2="orange"
        if mean_prob >=90:
            color2="red"
        tupla = (name, pers_prob, mean_prob, color, color2)
    return tupla

def correlation():
    personality = db.session.query(Formdata).all()
    number_of_people = []
    correlation_women = 0
    correlation_men = 0
    eyes_colors = []
    fitting1=" "
    fitting2=" "
    women_yes = []
    men_yes=[]
    for i in personality:
        number_of_people.append(i.sex)
        eyes_colors.append(i.eyes)
        number_of_women=number_of_people.count('1')
        number_of_men=number_of_people.count('0')
        if i.q1 == "Tak" and i.sex == '1':
            women_yes.append(1)
        positive_women=women_yes.count(1)

        try:
            correlation_women = round(positive_women/number_of_women,3)
        except ZeroDivisionError:
            correlation_women=0
        if correlation_women>0 and correlation_women<=0.2:
            fitting1="niewielka zgodność"
        elif correlation_women>=0.21 and correlation_women<=0.4:
            fitting1="znośna zgodność"
        elif correlation_women>=0.41 and correlation_women<=0.6:
            fitting1="umiarkowana zgodność"
        elif correlation_women>=0.61 and correlation_women<=0.8:
            fitting1="znaczna zgodność"
        elif correlation_women>=0.81 and correlation_women<=1:
            fitting1="prawie całkowita zgodność"

        if i.q1 == "Tak" and i.sex == '0':
            men_yes.append(0)
        positive_men=men_yes.count(0)
        try:
            correlation_men = round(positive_men/number_of_men,3)
        except ZeroDivisionError:
            correlation_men=0

        if correlation_men>0 and correlation_men<=0.2:
            fitting2="niewielka zgodność"
        elif correlation_men>=0.21 and correlation_men<=0.4:
            fitting2="znośna zgodność"
        elif correlation_men>=0.41 and correlation_men<=0.6:
            fitting2="umiarkowana zgodność"
        elif correlation_men>=0.61 and correlation_men<=0.8:
            fitting2="znaczna zgodność"
        elif correlation_men>=0.81 and correlation_men<=1:
           fitting2="prawie całkowita zgodność"
    return eyes_colors

@app.route("/")
def welcome():
    return render_template('index.html')


@app.route("/form")
def form():
    return render_template('form.html')


@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/save", methods=['POST'])
def save():
    id = request.form.get('id')
    firstname = request.form.get('firstname')
    email = request.form.get('email')
    age = request.form.get('age')
    eyes = request.form.get('eyes')
    sex = request.form.get('sex')
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')
    q7 = request.form.get('q7')
    q8 = request.form.get('q8')
    q9 = request.form.get('q9')

    fd = Formdata(id=id, firstname=firstname, email=email, sex=sex, eyes=eyes, age=age, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9)

    db.session.add(fd)
    db.session.commit()




    personality = db.session.query(Formdata).all()
    no_of_women = []
    for i in personality:
        nr_id = i.id
        if i.sex == "Kobieta":
            no_of_women.append(1)
            # ilosc=no_of_women.count(1)
    tupla=()
    tupla = probability_for_one()
    eyes_color=correlation()

    return render_template('result.html', firstname=firstname, id=nr_id, name=tupla[0], pers_prob=tupla[1], mean_prob=tupla[2], color=tupla[3], color2=tupla[4], eyes_color=eyes_color)

@app.route("/whole_results")
def result():
    tupla=()
    personality = db.session.query(Formdata).all()
    for i in personality:
        nr_id = i.id
    tupla = probability_for_one()
    return render_template('whole_results.html', id=nr_id, mean_prob=tupla[2], color2=tupla[4])


if __name__ == "__main__":
    app.debug = True
    app.run()

