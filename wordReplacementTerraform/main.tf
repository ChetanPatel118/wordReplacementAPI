#START:: Terrafrom code related to lambda function
#Lambda creation
resource "aws_lambda_function" "word_replacement_lambda"{
  function_name = var.function_name
  description = var.description
  s3_bucket = var.s3_bucket
  s3_key = var.s3_key
  handler = var.handler
  runtime = var.runtime
  memory_size = var.memory_size
  timeout = var.timeout
  role = aws_iam_role.lambda_execution_role.arn
  environment {
    variables = var.environment_variables
  }
  tags = var.required_tags
}


# Cloudwatch log group
resource "aws_cloudwatch_log_group" "log_group" {
  name = "/aws/lambda/${var.function_name}"
  retention_in_days = var.log_group_retention_in_days
}

# Lambda execution role creation
resource "aws_iam_role" "lambda_execution_role" {
    name = var.rolename
    assume_role_policy = file("iam_policy.json")
    managed_policy_arns = var.managed_policy_arns
}

#END:: Terrafrom code related to lambda function


# START:: Terrafrom code  for creation of AWS API Gateway
# API Creation
resource "aws_api_gateway_rest_api" "api" {
 name = var.api_gateway_name
 description = "Proxy to handle requests to our API"
}

# Resource Creation
resource "aws_api_gateway_resource" "apiresource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "wordreplacement"
}

# Method Creation
resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.apiresource.id
  http_method   = "GET"
  authorization = "NONE"
  request_parameters = {
  "method.request.path.proxy" = true
  }
}

# Integration
resource "aws_api_gateway_integration" "integration" {
  rest_api_id          = aws_api_gateway_rest_api.api.id
  resource_id          = aws_api_gateway_resource.apiresource.id
  http_method          = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.word_replacement_lambda.invoke_arn

}

# Method response
resource "aws_api_gateway_method_response" "response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.apiresource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
}

# Integration response
resource "aws_api_gateway_integration_response" "integrationresponse" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.apiresource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = aws_api_gateway_method_response.response.status_code
  depends_on = [aws_api_gateway_integration.integration]
}

# deployment
resource "aws_api_gateway_deployment" "apideployment" {
  depends_on = [aws_api_gateway_integration.integration]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name = var.stage_name
}

# Lambda invocation Permission
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.word_replacement_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:us-east-1:896852826619:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.apiresource.path}"
}
# END:: Terrafrom code  for creation of AWS API Gateway
