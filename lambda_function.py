import json
import boto3
import base64
import datetime
import sns_func
import csv
import os

from datetime import date
from botocore.exceptions import ClientError
iam = boto3.client('iam')
days_filter=10

                
def list_access_key(user, days_filter, status_filter):
    keydetails=iam_client.list_access_keys(UserName=user)
    key_details={}
    user_iam_details=[]
    
    # Some user may have 2 access keys.
    for keys in keydetails['AccessKeyMetadata']:
        if (days:=time_diff(keys['CreateDate'])) >= 1 and keys['Status']==status_filter:
            key_details['UserName']=keys['UserName']
            key_details['AccessKeyId']=keys['AccessKeyId']
            key_details['days']=days
            key_details['status']=keys['Status']
            user_iam_details.append(key_details)
            key_details={}
    return user_iam_details

def time_diff(keycreatedtime):
    now=datetime.datetime.now(datetime.timezone.utc)
    diff=now-keycreatedtime
    return diff.days

def create_key(uname):
    try:
        IAM_UserName=uname
        key = len(iam.list_access_keys(UserName=IAM_UserName)['AccessKeyMetadata'])
        if key == 2:
          keydetails=iam.list_access_keys(UserName=uname)
          for keys in keydetails['AccessKeyMetadata']:
            if (days:=time_diff(keys['CreateDate'])) >= days_filter:
                key_uname=keys['UserName']
                key_id=keys['AccessKeyId']
                print(os.path.join('/tmp/','accesskey.csv'))
                sns_func.notify_mail(key_uname,key_id,)
        else:
            response = iam.create_access_key(UserName=IAM_UserName)
            AccessKey = response['AccessKey']['AccessKeyId']
            SecretKey = response['AccessKey']['SecretAccessKey']
            json_data=json.dumps({'AccessKey':AccessKey,'SecretKey':SecretKey})
            resp = json.loads(json_data)
            access_data = resp['AccessKey']
            secret_data = resp['SecretKey']
            print(access_data,secret_data)
            print(os.path.join('/tmp','credentials.csv'))
            with open(os.path.join('/tmp/','credentials.csv'), 'w+') as fp:
                fieldnames = ['Username','AccessKey', 'SecretKey']
                thewriter = csv.DictWriter(fp, fieldnames=fieldnames)
                thewriter.writeheader()
                thewriter.writerow({'Username' : uname, 'AccessKey' : access_data,'SecretKey' : secret_data})
            sns_func.send_email(uname)
    except ClientError as e:
        print (e)
        
def deactive_key(uname):
    try:
        IAM_UserName=uname
        keydetails=iam.list_access_keys(UserName=uname)
        for keys in keydetails['AccessKeyMetadata']:
            if (days:=time_diff(keys['CreateDate'])) >= 10:
                key_uname=keys['UserName']
                key_id=keys['AccessKeyId']
                iam.update_access_key(AccessKeyId=key_id,Status='Inactive',UserName=key_uname)
                print(key_uname,key_id)
                sns_func.dis_conf_mail(key_uname,key_id)
                print("Done .....")
        return
    except ClientError as e:
        print (e)

def delete_key(uname):
    try:
        IAM_UserName=uname
        keydetails=iam.list_access_keys(UserName=uname)
        for keys in keydetails['AccessKeyMetadata']:
            if (days:=time_diff(keys['CreateDate'])) >= days_filter and keys['Status']=='Inactive':
                key_uname=keys['UserName']
                key_id=keys['AccessKeyId']
                key_status=keys['Status']
                iam.delete_access_key (UserName=uname,AccessKeyId=key_id)
                print(key_uname,key_id,key_status)
                sns_func.del_conf_mail(key_uname,key_id)
                print("Done .....")
        return
    except ClientError as e:
        print (e)

def lambda_handler(event, context):
    # TODO implement
    response = iam.get_group(GroupName='KeyRotationUser')
    print(response['Group']['GroupName'])
    #list all users in that group
    for user in response['Users']:
        #print("UserName: {0}\nCreateDate: {1}\n".format(user['UserName'], user['CreateDate']))
        #status = create_key(user['UserName'])
        #print (status)
        faction=event ["action"]
        #    fuser_name=event ["username"]
        if faction == "create":
            status = create_key(user['UserName'])
            print (status)
        elif faction == "deactivate":
            status = deactive_key(user['UserName'])
            print (status)
        elif faction == "delete":
            status = delete_key(user['UserName'])
            print (status)
        
               
        
     
#     status = deactive_key("apoorva.tiwari@***.com")
#     print (status)
# #    status = create_key("apoorva.tiwari@***.com",0)
#    print (status)


