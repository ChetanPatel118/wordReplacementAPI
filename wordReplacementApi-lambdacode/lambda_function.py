import boto3
import logging
import  sys
import datetime
import json
import os,re

#Initializing Logger
logger=logging.getLogger()
logger.setLevel(logging.INFO)


#Defining environment variables
sendSnsException = os.getenv("sendSNSException")
topicArn = os.getenv("snsTopicArn")

#Initializing SNS
sns=boto3.client('sns')

def lambda_handler(event, context):
    """ main lambda handler function for getting the message from the event object"""
    
    errorDescDict = {'errorMessage':''}
    
    try:
        startTime = datetime.datetime.now()
        logger.info("Lambda_Handler:: Entering the handler")
        
        #Reading the input string
        input_str = event['queryStringParameters']['input']
        print("The original string is : " + str(input_str))
        
        #Reading the config file for list of companies
        configPath = os.environ['LAMBDA_TASK_ROOT'] + "/companies.txt"    #path of the file containing name of companies
        companies = open(configPath).read()
        listCompanies = companies.split(" ")[0].split("\n")
    
        input_str=replace_string (listCompanies,input_str)
        
        endTime = datetime.datetime.now()
        delta = endTime - startTime
        logger.info("Lambda_Handler:: Total Time taken for execution {} ms ".format(delta.total_seconds()*1000))
        
        return {
        'statusCode': 200,
        'body': (input_str)
        }
    
    except:
        logger.error(':: lambda handler :: following exception occured:' + str(sys.exc_info()))
        logger.info(':: lambda handler::  Exiting handler')
        errorDescDict['errorMessage'] = str(sys.exc_info())
        logger.info(':: lambda handler::  before invoking send_sns_exception')
        send_sns_exception(errorDescDict, context)
        logger.info(':: lambda handler::  After invoking send_sns_exception')
        
        return str(sys.exc_info())
        
        
def replace_string(listCompanies,input_str):
    """ this method is for replacing the string"""
    
    logger.info("replace_string:: Entering the Function")
    
    try: 
        for i in listCompanies:
            repl = i + u"\u00A9"
            subs = i                    # initializing substring to be replaced
            
            # re.IGNORECASE ignoring cases
            # compilation step to escape the word for all cases
            compiled = re.compile(re.escape(subs), re.IGNORECASE)
            input_str = compiled.sub(repl, input_str)
        
        print("Replaced String : " + str(input_str))
        return (input_str)
    
    except:
        logger.error(':: replace_string :: following exception occured:' + str(sys.exc_info()))
        logger.info(':: replace_string :: Exiting function')
        raise Exception(str(sys.exc_info()))


def send_sns_exception(errorDescDict, context):
    """ this method is for sending email notificaiton to subscribers in case of lambda failures"""
    
    try:
        logger.info("send_sns_exception :: Entering the Function")
        sns_error_message = '\n'
        sns_error_message = sns_error_message + context.function_name + ' lambda functios has failed, below are the failure details. Please take necessary action.'
        sns_error_message = sns_error_message + '\\nError Message'+'                    :  ' + errorDescDict['errorMessage']
        sns_error_message = sns_error_message + '\nLambda Function Name'+'    :  ' + context.function_name
        sns_error_message = sns_error_message + '\nRequestId'+'                           :  ' + context.aws_request_id
        sns_error_message = sns_error_message + '\nLog Stream Name'+'              :  ' + context.log_stream_name
        sns_error_message = sns_error_message + '\nLog Group Name'+'               :  ' + context.log_group_name
        logger.info("send_sns_exception :: Sending error message to SNS Topic: " + str(sns_error_message))
        
        if sendSnsException == "True":
            logger.info("send_sns_exception :: Sending error message to SNS Topic:" + topicArn)
            message_send = sns.publish(TopicArn=topicArn, Message=sns_error_message,Subject = context.function_name + ' :: Lambda failure notification')
            logger.info("send_sns_exception  :: response from sns:" + str(message_send))
    
    except:
        logger.error(':: send_sns_exception :: following exception occured:' + str(sys.exc_info()))
        logger.info(':: send_sns_exception:: Exiting function')
        raise Exception(str(sys.exc_info()))  

    
    