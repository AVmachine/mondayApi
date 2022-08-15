from dynamodb_json import json_util as json
from datetime import datetime
import uuid
import pandas as pd

import boto3

def insert_activity_db(userId, activity, carbonSaving, teamId, accountId):
    #For testing locally
    dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    #For deployment
    #dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    newUuid = uuid.uuid4()
    newDateTime = datetime.now()

    #Creates a new row in the CharityInfo table
    activityInfo = {
        "TableName": "Activity",
        "Item": {
            "ActivityId": {"S": str(newUuid)},
            "UserId": {"S": userId},
            "Activity_Performed": {"S": activity},
            "Carbon_Saving": {"N": carbonSaving},
            "Insert_At": {"S": str(newDateTime)},
            "Team_Id": {"S": teamId},
            "Account_Id": {"S":accountId}
        }
    }

    try:
        response = dynamodb_client_local.put_item(**activityInfo)
        print("Successfully put item.")
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])

def get_single_user_info(userId):
    #For testing locally
    dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    #For Deployment
    #dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    try:
        response = dynamodb_client_local.scan(
            TableName="Activity",
            FilterExpression='#n = :n',
            ExpressionAttributeNames={
                "#n": "UserId"
            },
            ExpressionAttributeValues={
                ":n": {"S": userId}
            }
        )

        return response["Items"]
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response['Error']['Message']


def get_single_user_total_points_db(userId):
    userData = get_single_user_info(userId)
    df = pd.DataFrame(json.loads(userData))
    sumPoints = df['Carbon_Saving'].sum()
    return sumPoints

# def get_single_user_points_per_month_by_week(userId):
#     userData = get_single_user_info(userId)
#     df = pd.DataFrame(json.loads(userData))
#     sumPoints = df['Carbon_Saving'].sum()
#     return sumPoints