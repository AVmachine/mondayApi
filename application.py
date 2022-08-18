
from crypt import methods
from flask import Flask, request, jsonify

from queryFunctions import insert_activity_db, get_single_user_total_points_db, \
    get_single_user_points_per_month_by_week_db, get_teams_point_db, get_team_points_db

application = Flask(__name__)


@application.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@application.route('/insertActivity', methods=['POST'])
def insert_activity():
    requestData = request.get_json()
    insert_activity_db(requestData["userId"], requestData["Activity"], requestData["Carbon_Savings"], requestData["TeamId"], requestData["AccountId"])
    return 'true'

@application.route('/getSingleUserTotalPoints/<userId>', methods=['GET'])
def get_single_user_total_points(userId):
    totalPoints = get_single_user_total_points_db(str(userId))
    return str(totalPoints)

@application.route('/getSingleUserTotalPointsPerMonthByWeek', methods=['GET'])
def get_single_user_points_per_month_by_week():
    requestData = request.get_json()
    totalPoints = get_single_user_points_per_month_by_week_db(requestData["userId"])
    return totalPoints

@application.route('/getTeamsPoint', methods=['GET'])
def get_teams_points():
    teamData = get_teams_point_db()
    print(teamData)
    return teamData

@application.route('/getTeamPoints/<teamId>', methods=['GET'])
def get_team_points(teamId):
    teamData = get_team_points_db(teamId)
    print(teamData)
    return teamData

if __name__ == '__main__':
    application.debug = True
    application.run()


