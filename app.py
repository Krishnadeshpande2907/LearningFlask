from flask import Flask, request, make_response, render_template, redirect, url_for
import pandas as pd
import os
import uuid

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

@app.route('/convert_csv', methods=['POST'])
def convert_csv_two():
    file = request.files['file']

    df = pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename))

    return render_template('download.html', filename=filename)

@app.route('/page1')
def anotherRoute():
    return "<h1>This is Page 1</h1>"

@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route('/greeting')
def greeting():
    randomText = "random text"
    return render_template('greeting.html', text=randomText)

# @app.route('/add/<number1>/<number2>')
# def add(number1, number2):
#     return f"{number1} + {number2} = {number1 + number2}"

# adding 2 numbers like this concatenates them because they are strings

@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    return f"{number1} + {number2} = {number1 + number2}"

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f'<h1>{greeting}, {name}!</h1>'
    else:
        return "Missing greeting or name parameter!"

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return "You sent a POST request!"
    else:
        return "You sent a GET request!"
    
@app.route('/response')
def custom_response():
    response = make_response()
    response.status_code = 202
    response.headers['content-type'] = 'application/octet-stream'
    return response

# we can create a function/filters to be run in the html page 
# using Jinja2 templating
@app.template_filter('double')
def double_filter(n):
    return n * 2

# filter to have alternate uppercase and lowercase letters
@app.template_filter('alt_case')
def alt_case_filter(s):
    # result = ''
    # upper = True
    # for char in s:
    #     if char.isalpha():
    #         if upper:
    #             result += char.upper()
    #         else:
    #             result += char.lower()
    #         upper = not upper
    #     else:
    #         result += char
    # return result
    
    return ''.join(char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(s))
    
# can also redirect to other routes, handle errors, etc.
@app.redirect('/old-page')
def old_page():
    return redirect(url_for('index'))
# this can also be done in the html page using url_for

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)