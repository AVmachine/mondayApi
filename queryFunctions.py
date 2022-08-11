from datetime import datetime
import uuid

import boto3

def insert_activity_db(userId, activity, carbonSaving):
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
            "Insert_At": {"S": str(newDateTime)}
        }
    }

    try:
        response = dynamodb_client_local.put_item(**activityInfo)
        print("Successfully put item.")
        print(response)
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])