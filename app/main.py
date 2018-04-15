from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import serial
# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )

@app.route( '/' )
def hello():
  arduinoData = serial.Serial('COM41',9600)
  while (1==1):
          myData = (arduinoData.readline().strip())
          print (myData.decode('utf-8'))
  return render_template( './ChatApp.html' )

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  send(str( json ), broadcast=True)
  socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == '__main__':
  socketio.run( app, debug = True )