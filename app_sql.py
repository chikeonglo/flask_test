from flask import Flask, render_template, request, redirect, url_for
from flask_modus import Modus
import db

app = Flask(__name__)
modus = Modus(app)

@app.route('/snack', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.add_snack(request.form['name'], request.form['kind'])
        return redirect(url_for('index'))
    return render_template('sql_index.html', snacks=db.get_all_snacks())

@app.route('/snack/new')
def new():
    return render_template('crud_new.html')

@app.route('/snack/<int:ID>', methods=['GET', 'PATCH', 'DELETE'])
def show(ID):
    snacks = db.get_all_snacks()
    found_snack = next(snack for snack in snacks if snack[0] == ID)

    if request.method == b'PATCH':
        db.edit_snack(request.form['name'], request.form['kind'], ID)
        return redirect(url_for('index'))
    
    if request.method == b'DELETE':
        db.delete_snack(ID)
        return redirect(url_for('index'))
    
    return render_template('sql_show.html', snack=found_snack)

@app.route('/snack/<int:ID>/edit')
def edit(ID):
    snacks = db.get_all_snacks()
    found_snack = next(snack for snack in snacks if snack[0] == ID)
    return render_template('sql_edit.html', snack=found_snack)

