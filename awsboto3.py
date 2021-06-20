import boto3

class S3_Client:
    def __init__(self):
        # The calls to AWS STS AssumeRole must be signed with the access key ID
        # and secret access key of an existing IAM user or by using existing temporary
        # credentials such as those from another role. (You cannot call AssumeRole
        # with the access key for the root account.) The credentials can be in
        # environment variables or in a configuration file and will be discovered
        # automatically by the boto3.client() function. For more information, see the
        # Python SDK documentation:
        # http://boto3.readthedocs.io/en/latest/reference/services/sts.html#client

        # create an STS client object that represents a live connection to the
        # STS service
        # sts_client = boto3.client('sts',region_name='us-east-1')
        self.sts_client = boto3.client('sts')
        self.s3_resource = None
        self.s3_core = None
    """
    # # Call the assume_role method of the STSConnection object and pass the role
    # # ARN and a role session name.
    """
    def assume_role(self, role_arn):
        assumed_role_object = self.sts_client.assume_role(
            RoleArn = role_arn,
            RoleSessionName = "AssumeRoleSession1")

        # # From the response that contains the assumed role, get the temporary
        # # credentials that can be used to make subsequent API calls
        credentials = assumed_role_object['Credentials']

        # Use the temporary credentials that AssumeRole returns to make a
        # connection to Amazon S3
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
        self.s3_core = boto3.client(
            's3',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )

    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    def upload_file(self,file_name,bucket,object_name=None):
        print(f"Source file is {file_name}")
        print(f"Bucket name  is {bucket}")
        print(f"Target object path is {object_name}")

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name
        # Upload the file
        self.s3_resource.Bucket(bucket).upload_file(file_name, object_name)

    """List objects in a bucket
    :param bucket_name: Name of bucket to inspect for obects
    """
    def bucket_object_list(self, bucket_name):
        print(f"These are the objects bucket: {bucket_name}")
        response = self.s3_core.list_objects_v2(Bucket=bucket_name)
        # for obj in response['Contents']:
        #     print(obj['Key'])
        for obj in response.get('Contents',[]):
            if len(obj['Key']) > 0:
                print(obj['Key'])

    """Create Bucket
    :param bucket_name: Name of new bucket
    """
    def create_bucket(self, bucket_name):
        self.s3_resource.create_bucket(Bucket=bucket_name)

    """Delete Bucket
    :param bucket_name: Name of new bucket
    """
    def delete_bucket(self, bucket_name):
        # call method to access bucket first and
        # only then delete -- method to be built
        bucket = self.s3_resource.Bucket(bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    """
    Copy bucket contents to another
    :param bucket_name_source: Name of source bucket
    :param bucket_name_target: Name of targe bucket
    """
    def copy_bucket_contents(self, source_bucket_name, target_bucket_name):
        print(f"Source bucket is {source_bucket_name}")
        print(f"Source bucket is {target_bucket_name}")

        for key in self.s3_core.list_objects_v2(Bucket=source_bucket_name)['Contents']:
            files = key['Key']
            copy_source = {'Bucket': source_bucket_name,'Key': files}
            self.s3_resource.meta.client.copy(copy_source, target_bucket_name, files)
            print(files)

    """List all buckets
    """
    def list_all_buckets(self):
        for bucket in self.s3_resource.buckets.all():
            print(bucket.name)

    """Accessing a bucket
    """
    def access_bucket(self, bucket_name):
        # # Boto3
        # import botocore
        # bucket = s3.Bucket('mybucket')
        # exists = True
        # try:
        #     s3.meta.client.head_bucket(Bucket='mybucket')
        # except botocore.exceptions.ClientError as e:
        #     # If a client error is thrown, then check that it was a 404 error.
        #     # If it was a 404 error, then the bucket does not exist.
        #     error_code = e.response['Error']['Code']
        #     if error_code == '404':
        #         exists = False
        pass