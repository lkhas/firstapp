from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, escape
from firebase import firebase
import json
import pandas as pd
import matplotlib
import pyrebase
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = 'AMACHIabs'

firebase = firebase.FirebaseApplication('https://pmkvy-f880a.firebaseio.com', authentication=None)
activities = firebase.get('/Activities', None)
user = firebase.get('/Users', None)
config = {
    "apiKey": "AIzaSyB9Dt2ekz6_SvUnS6lTE_rgiI6JgUPRS8c",
    "authDomain": "pmkvy-f880a.firebaseapp.com",
    "databaseURL": "https://pmkvy-f880a.firebaseio.com",
    "projectId": "pmkvy-f880a",
    "storageBucket": "pmkvy-f880a.appspot.com",
    "messagingSenderId": "1060305725577"
}
fire_storage = pyrebase.initialize_app(config)
storage = fire_storage.storage()
print(user)
data = []
act_csv = []


@app.route('/')
def home():

    if 'username' not in session:

        return render_template('login.html')
    if 'username' in session:
        username = session['username']


    use = []
    for i in user.keys():
        use.append(i)
    for v in activities.values():
        for i in user:
            if i == v['conducted_by']:
                # print(user[i]['uname'])
                uname = user[i]['uname']
                activity = v['upload'], v['Activity_type'], v['Center'], v['Role'], v['activities_complete_today'], v[
                    'bool_experience_challenge'], \
                    v['challenge_handle_situation'], uname, v['could_improved'], v['curriculum'], v[
                        'end_date'], \
                    v['end_time'], v['feedback'], v['hashtag'], \
                    v['logdate'], v['logtime'], v['right_student_performance'], v['start_date'], v['start_time'], \
                    v['support_student_objectives'], v['todays_objective'], v['topics_covered'], \
                    v['went_well']
                csv = v['Activity_type'], v['Center'], v['Role'], v['activities_complete_today'],\
                    v['bool_experience_challenge'], v['challenge_handle_situation'], uname, v['could_improved'],\
                    v['curriculum'], v['end_date'], v['end_time'], v['feedback'], v['hashtag'], \
                    v['logdate'], v['logtime'], v['right_student_performance'], v['start_date'], v['start_time'], \
                    v['support_student_objectives'], v['todays_objective'], v['topics_covered'], \
                    v['went_well']
        data.append(activity)
        act_csv.append(csv)
    return render_template('pmkvyactivities.html', rows=data)


@app.route('/json2csv', methods=['GET', 'POST'])
def json2csv():
    return json.dumps(act_csv)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    session.permanent = True
    session.pop('username', None)
    for u in user.values():
        if u['uemail'] == request.form['Name'] and request.form['Password'] == "admin":
            session['username'] = request.form['Name']
            for uname in user.values():
                if uname['uemail'] == request.form['Name']:
                    print(uname['uname'])
            return redirect(url_for('home'))

    else:
        return render_template('login.html')


@app.route('/piechart', methods=['GET', 'POST'])
def piechart():
    if 'username' not in session:

        return render_template('login.html')
    if 'username' in session:
        username = session['username']

    df = pd.DataFrame(activities)
    dft = df.T
    count_center = dft.groupby('Center').count()[['Activity_type']]
    print(count_center)
    pie_village = count_center['Activity_type']
    number_of_center = []
    for i in range(len(pie_village)):
        vil_name_count = pie_village[i]
        number_of_center.append(vil_name_count)
    print(number_of_center)

    total = sum(number_of_center)
    plot = pie_village.plot.pie(y='Center', figsize=(6, 6), autopct=lambda p: '{:.0f}'.format(p * total / 100),
                                counterclock=False, shadow=True)
    print(plot)
    fig = plot.get_figure()
    fig.savefig("static/images/myplot.png")
    return render_template('pmkvy_pie_center.html')


@app.route('/image', methods=['GET', 'POST'])
def image():
    img = request.form.get("code")
    img1 = request.form.get("img1")
    img2 = request.form.get("img2")
    img3 = request.form.get("img3")
    print(img)
    print(img2)
    print(img3)
    a = storage.child("e9qUqJDfaSQIxKZOJdLRArvrK5G22019-01-1616:49:27.941").get_url(None)
    print(a)

    return render_template('pmkvyimage.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)