from dynamodb_json import json_util as json_dy
import uuid
import pandas as pd
from datetime import datetime
import boto3
import os
import json

def create_dynamodb_client_local(region="us-east-1"):
    return boto3.client("dynamodb",
                        endpoint_url="http://localhost:8000",
                        region_name = 'us-east-1')

def create_dynamodb_client_cloud():
    return boto3.client("dynamodb",
                        region_name=os.environ['region'],
                        aws_access_key_id=os.environ['access_key'],
                        aws_secret_access_key=os.environ['secret_key'])

def insert_activity_db(userId, activity, carbonSaving, teamId, accountId):
    dynamodb_client = create_dynamodb_client_cloud()
    newUuid = uuid.uuid4()
    newDateTime = datetime.now()

    # Creates a new row in the CharityInfo table
    activityInfo = {
        "TableName": "Activity",
        "Item": {
            "ActivityId": {"S": str(newUuid)},
            "UserId": {"S": userId},
            "Activity_Performed": {"S": activity},
            "Carbon_Saving": {"N": carbonSaving},
            "Insert_At": {"S": str(newDateTime)},
            "TeamId": {"S": teamId},
            "AccountId": {"S": accountId},
        },
    }
    try:
        response = dynamodb_client.put_item(**activityInfo)
        print("Successfully put item.")
        # Handle response
    except BaseException as error:
        print(error)
        print("Unknown error while putting item: " + error.response["Error"]["Message"])


def get_single_user_info(userId):
    dynamodb_client = create_dynamodb_client_cloud()
    try:
        response = dynamodb_client.scan(
            TableName="Activity",
            FilterExpression="#n = :n",
            ExpressionAttributeNames={"#n": "UserId"},
            ExpressionAttributeValues={":n": {"S": userId}},
        )

        return response["Items"]
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response["Error"]["Message"]


def get_single_user_total_points_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json_dy.loads(userData))
    sumPoints = df["Carbon_Saving"].sum()
    return sumPoints


def get_single_user_points_per_month_by_week_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json_dy.loads(userData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby([pd.Grouper(key="Insert_At", freq="W-SUN")])["Carbon_Saving"].sum()
    jsonStr = df2.to_json()
    return jsonStr

def get_single_user_points_per_year_by_month_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json_dy.loads(userData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby([pd.Grouper(key="Insert_At", freq="M")])["Carbon_Saving"].sum()
    jsonStr = df2.to_json()
    return jsonStr


def get_teams():
    dynamodb_client = create_dynamodb_client_cloud()
    try:
        response = dynamodb_client.scan(TableName="Activity")
        return response["Items"]
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response["Error"]["Message"]


def get_team(teamId):
    dynamodb_client = create_dynamodb_client_cloud()
    try:
        response = dynamodb_client.scan(
            TableName= "Activity",
            FilterExpression= "#c0b33 = :c0b33",
            ProjectionExpression= "#c0b30,#c0b31,#c0b32,#c0b33",
            ExpressionAttributeNames= {"#c0b30": "Carbon_Saving", "#c0b31": "Activity_Performed",
                                       "#c0b32": "Insert_At", "#c0b33": "TeamId"},
            ExpressionAttributeValues= {":c0b33": {"S": teamId}}
        )
        return response["Items"]
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response["Error"]["Message"]


def get_teams_point_db():
    teamData = get_teams()
    df = pd.DataFrame(json_dy.loads(teamData))
    df2 = df.groupby([pd.Grouper(key="TeamId")])["Carbon_Saving"].sum()
    return df2.to_json()


def get_team_points_db(teamId):
    teamData = get_team(teamId)
    df = pd.DataFrame(json_dy.loads(teamData))
    df2 = df.groupby(["TeamId"])["Carbon_Saving"].sum()
    return df2.to_json()

def get_single_user_points_per_week_per_activity_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json_dy.loads(userData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df3 = df.groupby(["Activity_Performed", pd.Grouper(key="Insert_At", freq="W-SUN")])[
        "Carbon_Saving"
    ].sum()
    change_to = [ {"activity_performed":val[0][0],"insert_at":str(val[0][1]),"carbon_saving":val[1]} for index, val in enumerate(df3.iteritems())]
    return change_to
    

def get_single_user_points_ytd_by_activity_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json_dy.loads(userData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["Activity_Performed", pd.Grouper(key="Insert_At", freq="Y")],as_index=False)[
        "Carbon_Saving"
    ].sum()
    change_to = json.dumps(df2.to_dict(orient='records'))
    return change_to

def get_team_weekly_stats_db(teamId):
    teamData = get_team(teamId)
    df = pd.DataFrame(json_dy.loads(teamData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["Activity_Performed", pd.Grouper(key="Insert_At", freq="W-SUN")],as_index=False)[
        "Carbon_Saving"
    ].sum()
    change_to = json.dumps(df2.to_dict(orient='records'))
    return change_to

def get_team_monthly_stats_db(teamId):
    teamData = get_team(teamId)
    df = pd.DataFrame(json_dy.loads(teamData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["Activity_Performed", pd.Grouper(key="Insert_At", freq="M")], as_index=False)[
        "Carbon_Saving"
    ].sum()
    return json.dumps(df2.to_dict(orient='records'))

def get_leaderboard_stats(accountId):
    dynamodb_client = create_dynamodb_client_cloud()
    try:
        response = dynamodb_client.scan(
            TableName="Activity",
            FilterExpression="#c58a0 = :c58a0",
            ExpressionAttributeNames={"#c58a0": "AccountId"},
            ExpressionAttributeValues={":c58a0": {"S": accountId}}
        )
        return response["Items"]
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response["Error"]["Message"]

def get_leaderboard_monthly_stats_db(accountId):
    monthyStats = get_leaderboard_stats(accountId)
    df = pd.DataFrame(json_dy.loads(monthyStats))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["UserId", pd.Grouper(key="Insert_At", freq="M")])[
        "Carbon_Saving"
    ].sum()
    return df2.to_json()

def get_leaderboard_monthly_stats_db(accountId):
    monthyStats = get_leaderboard_stats(accountId)
    df = pd.DataFrame(json_dy.loads(monthyStats))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["UserId", pd.Grouper(key="Insert_At", freq="M")], as_index=False)[
        "Carbon_Saving"
    ].sum()
    change_to = json.dumps(df2.to_dict(orient='records'))
    return change_to

def get_leaderboard_yearly_stats_db(accountId):
    yearlyStats = get_leaderboard_stats(accountId)
    df = pd.DataFrame(json_dy.loads(yearlyStats))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["UserId", pd.Grouper(key="Insert_At", freq="Y")], as_index=False)[
        "Carbon_Saving"
    ].sum()
    change_to = json.dumps(df2.to_dict(orient='records'))
    return change_to

def get_team_leaderboard_monthly_stats_db(accountId):
    monthyTeamStats = get_leaderboard_stats(accountId)
    df = pd.DataFrame(json_dy.loads(monthyTeamStats))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["TeamId", pd.Grouper(key="Insert_At", freq="M")], as_index=False)[
        "Carbon_Saving"
    ].sum()
    change_to = json.dumps(df2.to_dict(orient='records'))
    return change_to

def get_team_leaderboard_yearly_stats_db(accountId):
    yearlyTeamStats = get_leaderboard_stats(accountId)
    df = pd.DataFrame(json_dy.loads(yearlyTeamStats))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["TeamId", pd.Grouper(key="Insert_At", freq="Y")], as_index=False)[
        "Carbon_Saving"
    ].sum()
    change_to = json.dumps(df2.to_dict(orient='records'))
    return change_to