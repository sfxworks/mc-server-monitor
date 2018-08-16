"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import sys

#define log file in first argument
#python application.py <log file path>
logfile = sys.argv[1]

__author__ = 'quantomworks'

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfc\xe0.\xfa\xf2\x18EG\xedo\xff[\xc7.\xd0\xfa'
app.config['DEBUG'] = False

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()
        
class LogReader(Thread):
    def __init__(self):
        self.delay = 1
        super(LogReader, self).__init__()
    
    def listenToLogs(self):
        cur = 0
        """
        Tail latest.log and send the data.
        Sort the emits based on the 3 outputs
        INFO
        WARN
        ERROR
        """
        def analyze_line(line):
            if line.find('ERROR]') > -1:
                print('Error:' + line)
                socketio.emit('sterr', {'line': line}, namespace='/log')  
                
            elif line.find('WARN]') > -1:
                print('Warning' + line)
                socketio.emit('stwarn', {'line': line}, namespace='/log')
                
            elif line.find('INFO]') > -1:
                print('Info' + line)
                socketio.emit('stout', {'line': line}, namespace='/log')
        
        while not thread_stop_event.isSet():
            try:
                with open(logfile) as f:
                    f.seek(0,2)
                    if f.tell() < cur:
                        f.seek(0,0)
                    else:
                        f.seek(cur,0)
                    for line in f:
                        analyze_line(line)
                    cur = f.tell()
            except IOError:
                pass
    def run(self):
        self.listenToLogs()


@app.route('/')

@socketio.on('connect', namespace='/log')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the log thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = LogReader()
        thread.start()

@socketio.on('disconnect', namespace='/log')
def test_disconnect():
    print('Client disconnected')

#Host and port defined at args 2 and 3 respectively
if __name__ == '__main__':
    socketio.run(app, host=sys.argv[2], port=sys.argv[3])
    