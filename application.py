from crypt import methods
from flask import Flask, request, jsonify

from queryFunctions import (
    insert_activity_db,
    get_single_user_total_points_db,
    get_single_user_points_per_month_by_week_db,
    get_teams_point_db,
    get_team_points_db,
    get_single_user_points_per_month_by_week_db,
    get_single_user_points_per_week_per_activity_db,
    get_team_weekly_stats_db, get_single_user_points_ytd_by_activity_db, get_leaderboard_monthly_stats_db,
    get_leaderboard_yearly_stats_db
)

application = Flask(__name__)


@application.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@application.route("/insertActivity", methods=["POST"])
def insert_activity():
    requestData = request.get_json()
    insert_activity_db(
        requestData["userId"],
        requestData["Activity"],
        requestData["Carbon_Savings"],
        requestData["TeamId"],
        requestData["AccountId"],
    )
    return "true"


@application.route("/getSingleUserTotalPoints/<userId>", methods=["GET"])
def get_single_user_total_points(userId):
    totalPoints = get_single_user_total_points_db(str(userId))
    return str(totalPoints)


@application.route("/getSingleUserTotalPointsPerMonthByWeek/<userId>", methods=["GET"])
def get_single_user_points_per_month_by_week(userId):
    listPointsMonthByWeek = get_single_user_points_per_month_by_week_db(str(userId))
    return listPointsMonthByWeek


@application.route("/getSingleUserTotalPointsPerYearByMonth/<userId>", methods=["GET"])
def get_single_user_points_per_year_by_month(userId):
    listPointsYearByMonth = get_single_user_points_per_month_by_week_db(str(userId))
    return listPointsYearByMonth

@application.route(
    "/getSingleUserTotalPointsPerWeekPerActivity/<userId>", methods=["GET"]
)
def get_single_user_points_per_week_per_activity(userId):
    listPointsMonthByActivity = get_single_user_points_per_week_per_activity_db(
        str(userId)
    )
    return listPointsMonthByActivity

@application.route(
    "/getSingleUserTotalPointsYTDByActivity/<userId>", methods=["GET"]
)
def get_single_user_points_ytd_by_activity(userId):
    listPointsYTDByActivity = get_single_user_points_ytd_by_activity_db(
        str(userId)
    )
    return listPointsYTDByActivity


@application.route("/getTeamsPoint", methods=["GET"])
def get_teams_points():
    teamData = get_teams_point_db()
    return teamData

@application.route("/getTeamPoints/<teamId>", methods=["GET"])
def get_team_points(teamId):
    teamData = get_team_points_db(teamId)
    return teamData

@application.route("/getTeamWeeklyStats/<teamId>", methods=["GET"])
def get_team_weekly_stats(teamId):
    teamData = get_team_weekly_stats_db(teamId)
    return teamData

@application.route("/getLeaderboardMonthlyStats/<accountId>", methods=["GET"])
def get_leaderboard_monthly_stats(accountId):
    monthlyStats = get_leaderboard_monthly_stats_db(accountId)
    return monthlyStats

@application.route("/getLeaderboardYearlyStats/<accountId>", methods=["GET"])
def get_leaderboard_yearly_stats(accountId):
    yearlyStats = get_leaderboard_yearly_stats_db(accountId)
    return yearlyStats


if __name__ == "__main__":
    application.debug = True
    application.run()
