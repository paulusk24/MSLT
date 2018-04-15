import json
#import flask class from the flask module
from flask import (Flask,render_template,redirect,
                url_for,request,make_response,session,flash,g)
from flask_socketio import SocketIO,emit, send
from functools import wraps
import serial
#create application object
app = Flask(__name__)
#set a secret key
app.secret_key = 'Johnny Depp'
app.config['SECRET KEY'] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )



#login requred decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for ('login'))
    return wrap

@app.route('/login',methods=['GET', 'POST'])

def login():
  error = None
  if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
          error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True 
            flash('You were just logged in!')
            return redirect(url_for('home'))
  return render_template('login.html',error=error)

#use decorators t link the function to the url
@app.route('/home')
@login_required
def home():
        return render_template('home.html')

@app.route('/register')
@login_required
def register():
        return render_template('register.html')

@app.route('/patient')
@login_required
def business():
        return render_template('patient.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

@app.route('/chat')
#@login_required
def hello():
  return render_template( './ChatApp.html' )
def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  send(str( json ), broadcast=True)
  socketio.emit( 'my response', json, callback=messageRecived )



if __name__ == '__main__':
  socketio.run(app,debug=True)