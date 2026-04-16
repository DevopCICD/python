import json
import os
import boto3

sns_client = boto3.client("sns")

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):
    try:
        # Extract EC2 event details
        detail = event.get("detail", {})
        instance_id = detail.get("instance-id", "Unknown")
        state = detail.get("state", "Unknown")
        region = event.get("region", "Unknown")
        time = event.get("time", "Unknown")

        message = (
            f"EC2 Instance State Change Detected\n\n"
            f"Instance ID : {instance_id}\n"
            f"State       : {state}\n"
            f"Region      : {region}\n"
            f"Time        : {time}"
        )

        # Send SNS notification
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EC2 Instance Event Notification",
            Message=message
        )

        return {
            "statusCode": 200,
            "body": json.dumps("Notification sent successfully")
        }

    except Exception as e:
        print("Error:", str(e))
        raise
