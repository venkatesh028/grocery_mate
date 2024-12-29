import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from config import Config
from logger import setup_logger

log = setup_logger()

client = boto3.client(
         service_name='s3',
         aws_access_key_id='test',
         aws_secret_access_key='test',
         endpoint_url='http://localhost:4566',
)


def upload_file(data, key, bucket=Config.S3_BUCKET_NAME):
    try:
        response = client.put_object(Body=data, Bucket=bucket, Key=key)
    except ClientError as e:
        log.error(e)
        return False
    return response


def generate_presigned_url(file_key):

    try:
        # Generate a presigned URL (with no expiration)
        presigned_url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': Config.S3_BUCKET_NAME, 'Key': file_key},
            ExpiresIn=0  # No expiry (forever)
        )
        return presigned_url
    except NoCredentialsError:
        raise Exception("S3 credentials not found or invalid")
