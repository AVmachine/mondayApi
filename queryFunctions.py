from dynamodb_json import json_util as json_dy
import uuid
import pandas as pd
from datetime import datetime
from boto3.dynamodb.conditions import Key
import boto3


def insert_activity_db(userId, activity, carbonSaving, teamId, accountId):
    # For testing locally
    dynamodb_client_local = boto3.client(
        "dynamodb", endpoint_url="http://localhost:8000"
    )
    # For deployment
    # dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

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
        response = dynamodb_client_local.put_item(**activityInfo)
        print("Successfully put item.")
        # Handle response
    except BaseException as error:
        print(error)
        print("Unknown error while putting item: " + error.response["Error"]["Message"])


def get_single_user_info(userId):
    # For testing locally
    dynamodb_client_local = boto3.client(
        "dynamodb", endpoint_url="http://localhost:8000"
    )
    # For Deployment
    # dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    try:
        response = dynamodb_client_local.scan(
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


def get_teams():
    dynamodb_client_local = boto3.client(
        "dynamodb", endpoint_url="http://localhost:8000"
    )
    try:
        response = dynamodb_client_local.scan(TableName="Activity")

        return response["Items"]
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response["Error"]["Message"]


def get_team(teamId):
    dynamodb_client_local = boto3.resource(
        "dynamodb", endpoint_url="http://localhost:8000"
    )
    try:
        table = dynamodb_client_local.Table("Activity")
        response = table.query(
            IndexName="ActivityGsi",
            KeyConditionExpression=Key("TeamId").eq(str(teamId)),
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
    df2 = df.groupby([pd.Grouper(key="TeamId")])["Carbon_Saving"].sum()
    return df2.to_json()


def get_single_user_points_per_week_per_activity_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json_dy.loads(userData))
    df["Insert_At"] = pd.to_datetime(df["Insert_At"])
    df2 = df.groupby(["Activity_Performed", pd.Grouper(key="Insert_At", freq="W-SUN")])[
        "Carbon_Saving"
    ].sum()
    jsonStr = df2.to_json()
    print(jsonStr)
    return jsonStr
