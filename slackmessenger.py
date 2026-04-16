import json
import os
import requests
from dateutil import parser as date_parser

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def lambda_handler(event, context):
    try:
        detail = event.get("detail", {})
        instance_id = detail.get("instance-id", "Unknown")
        state = detail.get("state", "Unknown")
        region = event.get("region", "Unknown")

        raw_time = event.get("time", "")
        event_time = date_parser.parse(raw_time).strftime("%Y-%m-%d %H:%M:%S UTC")

        # Slack message payload
        slack_payload = {
            "text": "*EC2 Instance State Change Detected*",
            "attachments": [
                {
                    "color": "#36a64f",
                    "fields": [
                        {"title": "Instance ID", "value": instance_id, "short": True},
                        {"title": "State", "value": state, "short": True},
                        {"title": "Region", "value": region, "short": True},
                        {"title": "Time", "value": event_time, "short": False}
                    ]
                }
            ]
        }

        response = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps(slack_payload),
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()

        return {
            "statusCode": 200,
            "body": json.dumps("Slack notification sent successfully")
        }

    except Exception as e:
        print("Error:", str(e))
        raise
