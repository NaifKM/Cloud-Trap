import os
import boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):
    detail = event["detail"]

    user = detail["userIdentity"].get("userName", "unknown")
    action = detail["eventName"]
    service = detail["eventSource"]
    ip = detail["sourceIPAddress"]
    region = detail["awsRegion"]
    when = detail["eventTime"]

    error = detail.get("errorCode")
    if error:
        result = f"denied ({error})"
    else:
        result = "succeeded"

    subject = f"Decoy key used: {user} called {action}"

    body = f"""Someone used the access key for {user}.
This is a decoy credential. Treat any use of it as a security incident.

Action:     {action} ({service})
Result:     {result}
Source IP:  {ip}
Region:     {region}
Time (UTC): {when}

Next steps:
- Check where this key was stored and who could read it
- Look up the source IP
- Review CloudTrail event history for {user}
"""

    sns.publish(TopicArn=TOPIC_ARN, Subject=subject, Message=body)
