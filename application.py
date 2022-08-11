from flask import Flask

from queryFunctions import insert_activity_db

application = Flask(__name__)


@application.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@application.route('/insertActivity')
def insert_activity():
    insert_activity_db("1234-1234-1234-1234", "Cycling", "1")
    return 'Success maybe'

if __name__ == '__main__':
    application.debug = True
    application.run()


