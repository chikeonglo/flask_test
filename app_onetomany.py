from flask import Flask, request, redirect, url_for, render_template
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/flask-sql-onetomany'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'users' # table name will default to name of the model

    # column names for table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    messages = db.relationship('Message', backref='user', lazy='dynamic') 
    # does not do anything on the database, simply tells flask how to handle relationship
        # find a specific user
            # user.messages
        # find a specific message
            # message.user
    
    # define each instance
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    
    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return f"First name is {self.first_name}, last name is {self.last_name}"

class Message(db.Model):

    __tablename__ = 'messages' # table name will default to name of the model

    # column names for table
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # define each instance
    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id

# User Portion
@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/user', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.session.add(User(request.form['first_name'], request.form['last_name']))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('users/otm_index.html', users=User.query.all())

@app.route('/user/new')
def new_user():
    return render_template('users/otm_new.html')

@app.route('/user/<int:id>/edit')
def edit_user(id):
    return render_template('users/otm_edit.html', user=User.query.get(id))

@app.route('/user/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def show_user(id):
    found_user = User.query.get(id)
    if request.method==b'PATCH':
        found_user.first_name = request.form['first_name']
        found_user.last_name = request.form['last_name']
        db.session.add(found_user)
        db.session.commit()
    
    if request.method==b'DELETE':
        db.session.delete(found_user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('users/otm_show.html', user=found_user)

# Message Portion
## create and see all messages for a user
@app.route('/user/<int:user_id>/messages', methods=['GET', 'POST'])
def msg_index(user_id):
    if request.method=='POST':
        db.session.add(Message(request.form['message'], user_id))
        db.session.commit()
        return redirect(url_for('msg_index', user_id=user_id))
    return render_template('messages/otm_index.html', user=User.query.get(user_id))

@app.route('/user/<int:user_id>/messages/new')
def msg_new(user_id):
    return render_template('messages/otm_new.html', user=User.query.get(user_id))

## edit message
@app.route('/user/<int:user_id>/messages/<int:id>/edit')
def msg_edit(user_id, id):
    pass

## delete message
@app.route('/user/<int:user_id>/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def msg_show(user_id, id):
    pass

