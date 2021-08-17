import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.charset import Charset, BASE64
from email.mime.nonmultipart import MIMENonMultipart
from email import charset



SENDER = "Sender Name <sender@domain.com>"

AWS_REGION = "eu-west-1"
AWS_SERVER_PUBLIC_KEY = "********************"
AWS_SERVER_SECRET_KEY = "##################################"


def send_email(email):
    
    SUBJECT = "Key Generation: AWS Access Key Rotation by DevOps"
    
    BODY_TEXT = "Hello,\r\nPlease find the attached file."
    # The HTML body of the email.
    
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <p> Hi </p>
    <p> Access Key  has been rotated and new <b>Access key</b> and <b>Secret Key</b> has been generate  for your AWS_Account.</p>
    <p> Secret Access Keys is attached in attachment .<br>
    Please find the attachment  .</p>
    <p> Please update this key as previous key will be disabled soon. <br>
        Notify DevOps( <u>sender@domain.com</u> ) in case of any issue.<br>
        Thank You </p>
        <p> Regards, <br>
            Sender.
        </p>
    </body>
    </html>
    """
    CHARSET = "utf-8"
    client  = boto3.client('ses',
             region_name=AWS_REGION,
             aws_access_key_id=AWS_SERVER_PUBLIC_KEY, 
             aws_secret_access_key=AWS_SERVER_SECRET_KEY)
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] =  SUBJECT
    msg['From'] = SENDER 
    msg['To'] = email
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open("/tmp/credentials.csv", 'rb').read())
    att.add_header('Content-Disposition','attachment',filename="credentials.csv")
    if os.path.exists("/tmp/credentials.csv"):
        print("File exists")
    else:
        print("File does not exists")
    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    # Add the attachment to the parent container.
    msg.attach(att)
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=msg['From'],
            Destinations=[
                msg['To']
            ],
            RawMessage={
                'Data':msg.as_string(),
            }
        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        return(e.response['Error']['Message'])
    else:
        return("Email sent! Message ID:", response['MessageId'])


def send_conf_mail(email,AccessKey,SecretKey):

    RECIPIENT = email

    SUBJECT = "Key Generation: AWS Access Key Rotation by Sender"

    body_html ="""
    <html>
    <head></head>
    <body>
    <p> Hi, </p>
    <p> Access Key  has been rotated and new <b>Access key</b> and <b>Secret Key</b> for your AWS_Account.</p>
      <p>Below are details of New Access Key and Secret Key <br>
           </p>
        <p>
        - <b>Login:</b>   <u> https://###.signin.aws.amazon.com/console </u> <br>
        - <b>AccessKey:</b>  """+ AccessKey +"""  <br>
        - <b>SecretKey:</b>   """+ SecretKey +"""  <br>
        - <b>Email:</b>      """+ email +"""  <br>
        </p>
        <p> Please update this key as previous key will be disabled soon. <br>
            Notify Sender( <u>Sender@domain.com</u> ) in case of any issue.<br>
            Thank You </p>
        <p> Regards, <br>
           Sender.
        </p>
	  </body>
     </html>
    """
    CHARSET = "UTF-8"
    client  = boto3.client('ses',
             region_name=AWS_REGION,
             aws_access_key_id=AWS_SERVER_PUBLIC_KEY, 
             aws_secret_access_key=AWS_SERVER_SECRET_KEY)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def notify_mail(email, AccessKey):

    RECIPIENT = email

    SUBJECT = "Alert: AWS Access Key Rotation by Sender. "

    body_html ="""
    <html>
    <head></head>
    <body>
    <p> Hi, </p>
    <p>We need to rotate Access Key and generate new <b>Access key</b> and <b>Secret Key</b> for your AWS_Account.</p>
      <p> As your account  already have maximun number of  keys due to which new key is not generate. <br>
      This is to notify that one of Access Key pair will be deleted soon. <br>
      Details of Access Key which will be deleted soon:</p>
        <p>
        - <b>Login:</b>   <u> https://###.signin.aws.amazon.com/console </u> <br>
        - <b>AccessKey:</b>  """+ AccessKey +"""  <br>
        - <b>Email:</b>      """+ email +"""  <br>
        </p>
        <p> Notify Sender( <u>sender@domain.com</u> ) in case of any issue.<br>
            Thank You </p>
        <p> Regards, <br>
            Sender.
        </p>
	  </body>
     </html>
    """
    CHARSET = "UTF-8"
    client  = boto3.client('ses',
             region_name=AWS_REGION,
             aws_access_key_id=AWS_SERVER_PUBLIC_KEY, 
             aws_secret_access_key=AWS_SERVER_SECRET_KEY)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
		

def del_conf_mail(email,AccessKey):

    RECIPIENT = email

    SUBJECT = "Deletion of Old AWS Access Key by Sender"

    body_html ="""
    <html>
    <head></head>
    <body>
    <p> Hi, </p>
    <p>Previous<b>Access key</b> and <b>Secret Key</b> has been deleted for your AWS_Account.<br>
    Below are details of deleted Access Key:</p>
        <p>
        -<b> Login:   </b><u> https://###.signin.aws.amazon.com/console </u> <br>
        -<b> AccessKey: </b> """+ AccessKey +"""  <br>
        -<b> UserName:    </b>  """+ email +"""  <br>
        </p>
    <p> Please Notify Sender( <u>sender@domain.com</u> ) in case of any issue.<br>
        <br>
        Thank You </p>
        
        <p> Regards, <br>
        Sender.
        </p>
	  </body>
     </html>
    """
    CHARSET = "UTF-8"
    client  = boto3.client('ses',
             region_name=AWS_REGION,
             aws_access_key_id=AWS_SERVER_PUBLIC_KEY, 
             aws_secret_access_key=AWS_SERVER_SECRET_KEY)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
		
def dis_conf_mail(email,AccessKey):

    RECIPIENT = email

    SUBJECT = "Disabled AWS Access Key by Sender"

    body_html ="""
    <html>
    <head></head>
    <body>
    <p> Hi, <p>
    <p> Previous <b>Access key</b> and <b>Secret Key</b> has been disabled for your AWS_Account.<br>
      Below is the Access Key which has been disabled. <br>
        </p>
        <p>
        -<b> Login:   </b><u> https://###.signin.aws.amazon.com/console </u> <br>
        - <b>AccessKey:</b>  """+ AccessKey +"""  <br>
        -<b> UserName:    </b>  """+ email +"""  <br>
        </p>
        <p> Please note  this disabled  key  will be deleted  soon. <br>
          Notify Sender( <u>Sender@domain.com</u> ) in case of any issue.<br>
          <br>
          Thank You </p>
          
        <p> Regards, <br>
        Sender.
        </p>
	  </body>
     </html>
    """
    CHARSET = "UTF-8"
    client  = boto3.client('ses',
             region_name=AWS_REGION,
             aws_access_key_id=AWS_SERVER_PUBLIC_KEY, 
             aws_secret_access_key=AWS_SERVER_SECRET_KEY)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
