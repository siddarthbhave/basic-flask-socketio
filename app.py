from flask import Flask, render_template, flash
from flask_socketio import SocketIO, send
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key!!'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)


from models import History

@socketio.on('message')
def handleMessage(msg):
    if msg != 'New User has connected!':
        _msg = History(message=msg)
        db.session.add(_msg)
        db.session.commit()
        send(msg, broadcast=True)
    else:
        flash('New User has connected.')

@app.route('/')
@app.route('/home')
def home():
    messages = History.query.all()
    return render_template('index.html', url=os.environ.get('URL'), messages=messages)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'History':History}

if __name__ == '__main__':
    socketio.run(app)

