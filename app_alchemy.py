# %%
from flask import Flask, request, redirect, url_for, render_template
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

# %%
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/flask-sql-snack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db = SQLAlchemy(app)

# %%
# all models inherit from SQLAlchemy's db.model
class Snacks(db.Model):

    __tablename__ = 'snacks' # table name will default to name of the model

    # column names for table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    kind = db.Column(db.Text)

    # define each instance
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
    
    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return f"{self.name} is a type of {self.kind}"


# %%
@app.route('/snack', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.session.add(Snacks(request.form['name'], request.form['kind']))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('sqlalchemy_index.html', snacks=Snacks.query.all())

@app.route('/snack/new')
def new():
    return render_template('crud_new.html')

@app.route('/snack/<int:ID>', methods=['GET', 'PATCH', 'DELETE'])
def show(ID):
    found_snack = Snacks.query.get(ID)

    if request.method == b'PATCH':
        found_snack.name = request.form['name']
        found_snack.kind = request.form['kind']
        db.session.add(found_snack)
        db.session.commit()
        return redirect(url_for('index'))
    
    if request.method == b'DELETE':
        db.session.delete(found_snack)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('sqlalchemy_show.html', snack=found_snack)

@app.route('/snack/<int:ID>/edit')
def edit(ID):
    found_snack = Snacks.query.get(ID)
    return render_template('sqlalchemy_edit.html', snack=found_snack)