from botocore.exceptions import ClientError
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm
import argparse
import boto3
import os
import glob
from helpers import timer

load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")
bucket_folder_images = os.getenv("BUCKET_FOLDER_IMAGES")
bucket_folder_annotations = os.getenv("BUCKET_FOLDER_ANNOTATIONS")

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key
                      )


def upload(bucket_name, s3_client, file_path, bucket_folder=None, object_name=None):
    """
    This function uploads file to Amazon s3 bucket.
    :param str bucket_name: Bucket name where will be uploaded files
    :param (instance of the Boto3 S3 client) s3_client: s3 client
    :param str file_path: File to upload
    :param str bucket_folder: Folder name in the bucket
    :param str object_name: S3 object name. If not specified then file_name is use
    """

    if bucket_folder is None:
        # if object_name is not specified use file_name
        if object_name is None:
            object_name = os.path.basename(file_path)
        try:
            s3_client.upload_file(file_path, bucket_name, object_name)
        except ClientError as e:
            logger.error(e)
    else:
        # if object_name is not specified use file_name
        if object_name is None:
            object_name = os.path.basename(file_path)
            bucket_folder_path = '%s/%s' % (bucket_folder, object_name)
        try:
            s3_client.upload_file(file_path, bucket_name, bucket_folder_path)
        except ClientError as e:
            logger.error(e)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--folder_path', type=str,  help='The folder directory from where files will be uploaded. If this argument is passed then "file_path" argument should be None.')
    parser.add_argument('--bucket_name', type=str, default=bucket_name, help='AWS bucket name')
    parser.add_argument('--file_path', type=str, default=None, help='In case of uploading single file not files from a directory.')
    parser.add_argument('--bucket_folder', type=str, default=None, help='Folder name in the bucket. Also can be specified like this: home/txt')
    parser.add_argument('--object_name', type=str, default=None, help='S3 object name')
    parser.add_argument('--file_type', type=str, default='txt', help='Type of the files to be uploaded from given directory. Not applicable in case of uploading single file by passing "file_path" argumnent')

    args = parser.parse_args()

    if args.folder_path:
        file_names = glob.glob(os.path.join(args.folder_path, f'*.{args.file_type}'))
        if file_names:
            logger.info(f'Start to upload files to AWS: There are {len(file_names)} files to upload!')
        else:
            logger.info(f'There is no file in the {args.folder_path} directory. Check the folder path or add files!')
        for full_path in tqdm(file_names):
            upload(
             bucket_name=args.bucket_name, s3_client=s3, file_path=full_path, bucket_folder=args.bucket_folder, object_name=args.object_name, file_type=args.file_type)
        logger.success("Files has been successfully uploaded!")
    else:
        upload(
            bucket_name=args.bucket_name, s3_client=s3, file_path=args.file_path, bucket_folder=args.bucket_folder,
            object_name=args.object_name, file_type=args.file_type)
