Automate Access Key Rotation in IAM AWS using CloudWatch Events and Lambda Fucntion:

The components used to incorporate automatic IAM access key rotation into  IAM operations workflow:

1. Lambda :  generates API calls to IAM services to rotate and update keys.
2. CloudWatch: initiates events on a scheduled basis to rotate keys.
3. IAM: provides user access and secret keys for accessing AWS resources and services from non-AWS systems.
4. SNS: sends notifications whenever keys are changed.
5. Service Account - for Access and secret key 


![image](https://user-images.githubusercontent.com/84247031/118375297-90b3c600-b5de-11eb-99ed-378d062930df.png)

Once the components—IAM user with API key or secret, AWS Lambda functions, Amazon CloudWatch Events —are created, the solution follows these steps:
1. Every 80 days, a Lambda function creates a new key and save details in csv file(shared to user).
2. SNS updates the application owner that a key has been rotated.
3. After 90 days, the same Lambda function disables the old keys and a notification is sent to the user.
4. After 100 days, the old keys are deleted and notifications are sent to the user again.

**Setting Up the Key Rotation**
Automated key rotation is build based on the following policies:
• All IAM users in KeyRotation Group have to use new access key and secret key every 80 days.
• Deactivate previous access key and secret key every 90 days.
• Delete the previous access key and secret key every 100 days.

The keys lifecycle length can be customized based on our need by modifying the CloudWatch Event rules.
 Lambda function is created  and integrated it with CloudWatch Event Rules.

This Lambda function has three sub-functions:
Create_Key: This takes input from the CloudWatch Event for action , creates the key in IAM, and sends a notification to the subscribed user.
Deactive_Key: This takes input from the CloudWatch Event for user id, compares IAM access keys and deactivates whichever key is older, and sends a notification to the subscribed user.
Delete_Key: This takes input form the CloudWatch Event for user id, checks whichever key is deactivated and deletes the key, and sends a notification to the subscribed user.




