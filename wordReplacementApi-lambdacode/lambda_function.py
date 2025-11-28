import boto3
import logging
import os
import re
import json

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS
sns = boto3.client('sns')

# Configuration
SEND_SNS_EXCEPTION = os.getenv("sendSNSException", "False").lower() == "true"
TOPIC_ARN = os.getenv("snsTopicArn")

# Global state for cached companies
COMPANY_MAP = {}
REGEX_PATTERN = None

def load_companies():
    """Loads companies from file and compiles regex pattern."""
    global COMPANY_MAP, REGEX_PATTERN
    
    if COMPANY_MAP:
        return

    try:
        companies_file = os.path.join(os.environ.get('LAMBDA_TASK_ROOT', ''), 'companies.txt')
        logger.info(f"Loading companies from {companies_file}")
        
        with open(companies_file, 'r') as f:
            content = f.read()
            # Logic to match original parsing: take first part before space, then split by newline
            # This handles the case where there might be extra data after a space in the file
            raw_list = content.split(" ")[0].split("\n")
            
            for company in raw_list:
                company = company.strip()
                if company:
                    # Map lowercase to display version with copyright
                    COMPANY_MAP[company.lower()] = company + "\u00A9"
        
        if COMPANY_MAP:
            # Sort by length descending to match longest possible words first (good practice for regex)
            sorted_keys = sorted(COMPANY_MAP.keys(), key=len, reverse=True)
            pattern_str = r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b'
            REGEX_PATTERN = re.compile(pattern_str, re.IGNORECASE)
            
    except Exception as e:
        logger.error(f"Failed to load companies file: {e}")
        # We continue, as the lambda might still function without replacements or fail gracefully later

# Load on cold start
load_companies()

def lambda_handler(event, context):
    """Main lambda handler function."""
    logger.info("Lambda_Handler:: Entering the handler")
    
    try:
        # Input validation
        query_params = event.get('queryStringParameters')
        if not query_params or 'input' not in query_params:
             return {
              'statusCode': 400,
              'body': 'Error Message: Please use input as a queryStringParameter'
            }
        
        input_str = query_params['input']
        
        if not input_str:
             return {
              'statusCode': 204
            }

        # Replacement logic
        output_str = input_str
        if REGEX_PATTERN:
            def replace_callback(match):
                word = match.group(0)
                return COMPANY_MAP.get(word.lower(), word)
            
            output_str = REGEX_PATTERN.sub(replace_callback, input_str)

        return {
            'statusCode': 200,
            'body': output_str
        }

    except Exception as e:
        logger.exception("Lambda execution failed")
        send_sns_exception(str(e), context)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def send_sns_exception(error_message, context):
    """Sends SNS notification on failure."""
    try:
        if not SEND_SNS_EXCEPTION or not TOPIC_ARN:
            logger.info("SNS notification disabled or Topic ARN missing")
            return

        message = (
            f"{context.function_name} lambda function has failed, below are the failure details. Please take necessary action.\n\n"
            f"Error Message                    :  {error_message}\n"
            f"Lambda Function Name    :  {context.function_name}\n"
            f"RequestId                           :  {context.aws_request_id}\n"
            f"Log Stream Name              :  {context.log_stream_name}\n"
            f"Log Group Name               :  {context.log_group_name}"
        )
        
        logger.info(f"Sending error message to SNS Topic: {TOPIC_ARN}")
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject=f"{context.function_name} :: Lambda failure notification"
        )
        
    except Exception:
        logger.exception("Failed to send SNS notification")