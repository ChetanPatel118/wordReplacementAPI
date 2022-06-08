variable "function_name" {
  description = "Name of the lambda function"
}

variable "description" {
  description = "Description of the lambda function"
  default = "A generic lambda function"
}

variable "s3_bucket" {
  description = "Bucket containting the lambda code"
  default = null
}

variable "s3_key" {
  description = "The file name containing the lambda code"
  default = null
}

variable "handler" {
  description = "Path of the lambda handler"
  default = "lambda_function.lambda_handler"
}

variable "runtime" {
  description = "Runtime of the lambda function"
  default = "python3.7"
}

variable "memory_size" {
  description = "Memory allocated to the lambda function"
  default = 128
}

variable "timeout" {
  description = "Lambda timeout"
  default = 300
}

variable "rolename" {
  description = "Name of the role attached to the lambda function"
}

variable "environment_variables" {
  description = "Environment variables for the lambda function, should be in map format"
}

variable "required_tags" {
  description = "Tags to group the resources"
  type = object ({
    Project = string
    Owner = string
    })
}
variable "api_gateway_name" {
  description = "Name of the API Gateway"
  default = ""
}

variable "log_group_retention_in_days" {
  description = "Log group retention period"
  default = 30
}

variable "stage_name" {
  description = "The name of the stage for API deployment"
  default = ""
}

variable "managed_policy_arns" {
  description = "The policy arns to be attached to the lambda role"
  default = []
}
