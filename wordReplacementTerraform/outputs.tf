output "lambda_arn"{
  description = "ARN of the lambda function"
  value = aws_lambda_function.word_replacement_lambda.arn
}

output "lambda_invoke_arn" {
  description = "ARN to be used for invoking Lambda Function from API Gateway"
  value = aws_lambda_function.word_replacement_lambda.invoke_arn
}

output "api_url" {
  description = "The URL to invoke the API pointing to the stage"
  value       = aws_api_gateway_deployment.apideployment.invoke_url
}

output "creation_date" {
  description = "The creation date of the deployment"
  value = aws_api_gateway_deployment.apideployment.created_date
}
