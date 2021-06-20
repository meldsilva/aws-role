import logging
from awsboto3 import S3_Client


s3_client = S3_Client()
s3_client.assume_role("arn:aws:iam::465523221317:role/melos-s3-role")

# s3_client.upload_file("/Users/meldsilva/Documents/mel/large-dummyfile.txt",
#                       "josieandthecats",
#                       "large-dummyfile.txt")
s3_client.list_all_buckets()

# s3_client.copy_bucket_contents("josieandthecats","mel-bucket22")

# s3_client.list_all_buckets()
# s3_client.create_bucket("melosrilat2")

s3_client.bucket_object_list("josieandthecats")
s3_client.bucket_object_list("mel-bucket22")
