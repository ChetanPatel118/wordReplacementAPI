wordreplacementapi

Solution for word replacement api case

Assignment: Build an API that will use a string as input and does a find and replace for certain words and outputs the result. For example: replace Google for Google©.

Example input: “We really like the new security features of Google Cloud” 
Expected output: “We really like the new security features of Google Cloud©”

The words that need to be replaced are listed below: Oracle -> Oracle© Google -> Google© Microsoft -> Microsoft© Amazon -> Amazon© Deloitte -> Deloitte©

Solution:

The solution is deployed on AWS using services like AWS API Gateway and Lambda
The lambda is written is python language and the endpoint is hosted on AWS API gateway