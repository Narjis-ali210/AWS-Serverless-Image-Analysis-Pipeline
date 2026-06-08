# AWS Serverless Image Processing & AI Pipeline

An event-driven, serverless cloud architecture that automatically analyzes and tags uploaded images using artificial intelligence and stores the results in a NoSQL database.

Architecture Overview
The pipeline operates in a fully serverless manner, minimizing costs and maximizing scalability:
1. User uploads an image (`.jpg`) to an **Amazon S3 Bucket**.
2. S3 Trigger automatically invokes an **AWS Lambda** function upon successful upload.
3. AWS Lambda decodes the object key and sends the image metadata to **Amazon Rekognition**.
4. Amazon Rekognition performs object detection and labels extraction.
5. AWS Lambda saves the image name, extracted labels, and timestamp into an **Amazon DynamoDB** table.

Tech Stack
- Cloud Provider: Amazon Web Services (AWS)
- Compute: AWS Lambda (Python 3.x with Boto3)
- Storage: Amazon S3
- AI/ML Service: Amazon Rekognition
- Database: Amazon DynamoDB (NoSQL)
- Monitoring: Amazon CloudWatch Logs

 Challenges & Solutions Detailed During Testing
- Lambda Execution Timeout: The default 3-second timeout was insufficient for executing AI analysis and database writes consecutively. *Solution:* Handled and debugged via CloudWatch Logs, and optimized the function timeout setting to 10 seconds.
- URL-Encoded File Names:Special characters and spaces in S3 object keys caused `InvalidS3ObjectException`. *Solution:* Integrated Python's `urllib.parse` to properly decode object keys before passing them to the Rekognition API.
