
from flask import Flask, request

from queryFunctions import insert_activity_db, get_single_user_total_points_db

application = Flask(__name__)


@application.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@application.route('/insertActivity', methods=['POST'])
def insert_activity():
    requestData = request.get_json()
    insert_activity_db(requestData["userId"], requestData["Activity"], requestData["Carbon_Savings"], requestData["TeamId"], requestData["AccountId"])
    return 'true'

@application.route('/getSingleUserTotalPoints', methods=['GET'])
def get_single_user_total_points():
    totalPoints = get_single_user_total_points_db("1234-1234-1234-1234")
    return str(totalPoints)

if __name__ == '__main__':
    application.debug = True
    application.run()


