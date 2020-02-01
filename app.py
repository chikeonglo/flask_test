# from the flask library import a class named Flask
from flask import Flask, render_template, request, redirect, url_for
# web scrapping test
import requests
from scrapy import Selector
# CRUD test
from snack import Snack
from flask_modus import Modus
# create an instance of the Flask class
app = Flask(__name__)
modus = Modus(app)

# listen for a route to `/` - this is known as the root route
@app.route('/')
def base():
    return render_template('intro/intro_search.html')

@app.route('/person/<name>/<age>')
def person(name, age):
    return render_template('intro/intro_person.html', name=name, age=age)

@app.route('/calculate')
def calculate():
    return render_template('intro/intro_calc.html')

@app.route('/math')
def math():
    operation = request.args.get('operation')
    num1 = int(request.args.get('num1'))
    num2 = int(request.args.get('num2'))
    if operation == 'add':
        num_total = num1 + num2
    elif operation == 'substract':
        num_total = num1 - num2
    elif operation == 'multiply':
        num_total = num1 * num2
    elif operation == 'divide':
        num_total = num1 / num2
    else:
        num_total = 'Invalid Operation'
    return str(num_total)

@app.route('/results')
def results():
    search = request.args.get('search')
    url = 'https://news.google.com'
    html = requests.get(url).content
    sel = Selector(text = html)
    titles = sel.xpath('//h3/a/text()').getall()
    links = sel.xpath('//h3/a/@href').getall()
    keep_index= []
    for index, title in enumerate(titles):
        if search.lower() in title.lower():
            keep_index.append(index)
    lists = []
    for i in keep_index:
        t = titles[i]
        l = links[i]
        results = dict(titles = t, links = l)
        lists.append(results)
    return render_template('intro_results.html', lists=lists)

# CRUD testing
toblerone = Snack('toblerone', 'chocolate')
ferrero = Snack('ferrero rocher', 'chocolate')
sour_patch = Snack('sour patch', 'candy')

snacks = [toblerone, ferrero, sour_patch]

@app.route('/snack', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        snacks.append(Snack(request.form['name'], request.form['kind']))
        return redirect(url_for('index'))
    return render_template('intro/crud_index.html', snacks=snacks)

@app.route('/snack/new')
def new():
    return render_template('intro/crud_new.html')

@app.route('/snack/<int:ID>', methods=['GET', 'PATCH', 'DELETE'])
def show(ID):
    found_snack = next(snack for snack in snacks if snack.ID == ID)

    if request.method == b'PATCH':
        found_snack.name = request.form['name']
        found_snack.kind = request.form['kind']
        return redirect(url_for('index'))
    
    if request.method == b'DELETE':
        snacks.remove(found_snack)
        return redirect(url_for('index'))
    
    return render_template('intro/crud_show.html', snack=found_snack)

@app.route('/snack/<int:ID>/edit')
def edit(ID):
    found_snack = next(snack for snack in snacks if snack.ID == ID)
    return render_template('intro/crud_edit.html', snack=found_snack)

