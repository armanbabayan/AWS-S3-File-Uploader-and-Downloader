from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm
import argparse
import boto3
import os

from helpers import timer

load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")
bucket_folder_images = os.getenv("BUCKET_FOLDER_IMAGES")
bucket_folder_annotations = os.getenv("BUCKET_FOLDER_ANNOTATIONS")


@timer
def get_number_of_files(bucket_name: str, bucket_folder: str) -> tuple:
    """
    This function takes AWS bucket name and a folder name from that bucket
    and returns number of files and the names
    :param str bucket_name: AWS bucket name
    :param str bucket_folder: folder name
    :return tuple: first element is number of files, second element is the names of that files
    """
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

    paginator = s3_client.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=bucket_name, Prefix=bucket_folder)
    file_names = []
    count = 0
    for response in tqdm(response_iterator):
        if 'Contents' in response:
            files = response['Contents']
            for file in files:
                file_names.append(file['Key'].split("/")[-1])
                count += 1
    file_names = file_names[1::]
    return count, file_names


@timer
def download_objects(object_names: list, bucket_name: str, bucket_folder: str, save_dir: str):
    """
    This function takes object list as an input, bucket folder dir and the save path
    and downloads files from give AWS bucket to the specific directory
    :param list object_names: name of the files to be downloaded
    :param str bucket_folder: folder path from where to be downloaded the files
    :param str save_dir: the directory where should be saved the downloaded files
    :return: None
    """

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    for object_name in tqdm(object_names):
        bucket_folder_path = '%s/%s' % (bucket_folder, object_name)
        s3.download_file(bucket_name, bucket_folder_path,
                         os.path.join(save_dir, object_name))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket_name', type=str, default=bucket_name, help='AWS bucket name')
    parser.add_argument('--bucket_folder_images', type=str, default=bucket_folder_images,
                        help='Folder name of the images in the bucket')
    parser.add_argument('--bucket_folder_annotations', type=str, default=bucket_folder_annotations,
                        help='Folder name of the annotations in the bucket')
    parser.add_argument('--save_dir_images', type=str, help='The directory path to save downloaded images.')
    parser.add_argument('--save_dir_annot', type=str, help='The directory path to save downloaded annotations.')
    parser.add_argument('--number_of_files', type=int, default=None,
                        help='Number of files to be downloaded.')

    args = parser.parse_args()

    image_count, image_names = get_number_of_files(bucket_name=args.bucket_name, bucket_folder=args.bucket_folder_images)
    logger.info(f"Number of files in the folder: {image_count}")

    if args.number_of_files is not None:
        image_names = image_names[:int(args.number_of_files)]
        print(type(int(args.number_of_files)))
        print(f"len {len(image_names)}")
        annotations = [name.replace(".png", ".txt") for name in image_names]
    else:
        annotations = [name.replace(".png", ".txt") for name in image_names]
    logger.info("Start downloading files...")
    logger.info(f"Number of images to be downloaded: {len(image_names)}")
    logger.info(f"Number of annotations to be downloaded: {len(annotations)}")
    download_objects(
                     object_names=image_names,
                     bucket_name=args.bucket_name,
                     bucket_folder=args.bucket_folder_images,
                     save_dir=args.save_dir_images
                     )
    download_objects(
                     object_names=annotations,
                     bucket_name=args.bucket_name,
                     bucket_folder=args.bucket_folder_annotations,
                     save_dir=args.save_dir_annot
                     )
    logger.info("Downloading finished successfully!")

