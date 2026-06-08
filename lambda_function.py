import boto3
import json
from datetime import datetime
import urllib.parse

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    rekognition_client = boto3.client('rekognition')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('imaqanalysis')
    
    # اسم الصورة من الـ event مع فك التشفير
    bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']
    image_name = urllib.parse.unquote_plus(raw_key)
    
    # تحليل الصورة باستخدام Rekognition
    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
        MaxLabels=10
    )
    
    # استخراج التسميات
    labels = [label['Name'] for label in response['Labels']]
    
    # حفظ النتائج في DynamoDB
    table.put_item(Item={
        'ImageName': image_name,
        'Labels': json.dumps(labels),
        'Timestamp': datetime.now().isoformat()
    })
    
    return {'statusCode': 200, 'body': json.dumps(labels)}
