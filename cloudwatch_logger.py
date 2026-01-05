import boto3
import time

logs_client = boto3.client("logs")


def create_log_stream(log_group, log_stream):
    """
    Creates a CloudWatch log stream if it does not exist
    """
    try:
        logs_client.create_log_stream(
            logGroupName=log_group,
            logStreamName=log_stream
        )
    except logs_client.exceptions.ResourceAlreadyExistsException:
        pass  # Stream already exists


def log_message(log_group, log_stream, message):
    """
    Pushes a log event to CloudWatch Logs
    """
    timestamp = int(time.time() * 1000)

    try:
        logs_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    "timestamp": timestamp,
                    "message": message
                }
            ]
        )
    except logs_client.exceptions.InvalidSequenceTokenException:
        # Fetch sequence token and retry (simple approach)
        response = logs_client.describe_log_streams(
            logGroupName=log_group,
            logStreamNamePrefix=log_stream
        )
        sequence_token = response["logStreams"][0]["uploadSequenceToken"]

        logs_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    "timestamp": timestamp,
                    "message": message
                }
            ],
            sequenceToken=sequence_token
        )
