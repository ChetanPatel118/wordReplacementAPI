import sys
import os
import logging
import json

# Mock environment variables
os.environ['LAMBDA_TASK_ROOT'] = os.getcwd()
os.environ['sendSNSException'] = 'False'
os.environ['snsTopicArn'] = 'arn:aws:sns:us-east-1:123456789012:test-topic'

# Mock boto3
from unittest.mock import MagicMock
sys.modules['boto3'] = MagicMock()

# Import the lambda function
import lambda_function

# Mock Context object
class MockContext:
    def __init__(self):
        self.function_name = "test_function"
        self.aws_request_id = "test_request_id"
        self.log_stream_name = "test_log_stream"
        self.log_group_name = "test_log_group"

def test_lambda(input_str):
    print(f"Testing with input: '{input_str}'")
    event = {
        'queryStringParameters': {
            'input': input_str
        }
    }
    context = MockContext()
    try:
        response = lambda_function.lambda_handler(event, context)
        print(f"Response: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"Execution failed: {e}")
    print("-" * 20)

if __name__ == "__main__":
    # Test cases
    test_lambda("Hello Google and Microsoft")
    test_lambda("No match here")
    test_lambda("oracle is a company")
    test_lambda("")
