# Variables for the lambda function
function_name = "wordReplacementApi"
description = "Lambda for replacing certain words from input string"
s3_bucket = "myownclusterbucket"
s3_key = "wordReplacementApi-9eef03f6-05b2-4bac-a52f-07211e5df09d.zip"
handler = "lambda_function.lambda_handler"
runtime = "python3.9"
memory_size = 128
timeout = 60
rolename = "wordReplacementLambdaExecution"
environment_variables = {
  sendSNSException = "True",
  snsTopicArn = "arn:aws:sns:us-east-1:896852826619:lambda-failures"
}
required_tags = {
  Project = "Deloitte"
  Owner = "Chetan"
}
managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole", "arn:aws:iam::896852826619:policy/SNSPublishPolicy"]


# Variables for the API Gateway
log_group_retention_in_days=30
api_gateway_name= "wordReplacementApi"
stage_name = "test"
