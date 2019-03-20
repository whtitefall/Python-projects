import boto3 

# Access_Key_ID =  ''
# Secret_Access_Key =  ''
# Buckget_Name = 'yuanzhenghu'
# data = open('test.txt','rb')
# s3 = boto3.resource('s3',
#             aws_access_key_id = Access_Key_ID,
#             aws_secret_access_key = Secret_Access_Key)
# s3.Bucket(Buckget_Name).put_object(Key = 'test.txt',Body = data)

s3 = boto3.client('s3')
filename = 'file.txt'
bucket_name = 'yuanzhenghu'
s3.upload_file(filename, bucket_name, filename)


print ('Done')
