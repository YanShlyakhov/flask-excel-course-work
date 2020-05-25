import pandas
import os
import json
from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = '/'

def is_time(value):
    return ":" in str(value)

def from_h_m_to_time(string):
    if not is_time(string):
        return string    
    h,m,s = string.split(':')  
    return int(h)*60 + int(m)

def json_generate(path):
    excel_data_df = pandas.read_excel(path)

    json_str = eval(excel_data_df.to_json())

    json_dicts = {}

    for key in json_str.keys():
        json_dicts[key] = [from_h_m_to_time(x) for x in json_str[key].values()]

    json_data = json.dumps(json_dicts, ensure_ascii=False)

    return json_data, list(json_dicts.keys())


@app.route('/template')
def template():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        json_data, headers = json_generate('kek.xlsx')
        print(headers)
        print(json_data)
        return render_template('index.html', json_data=json_data, headers=headers, count_of_headers=len(headers))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "No selected files"
        filename = "kek.xlsx"
        file.save(filename)
        return redirect(url_for('template'))
    return "Invalid file"


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return template()


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()



if __name__ == '__main__':
    app.run()
