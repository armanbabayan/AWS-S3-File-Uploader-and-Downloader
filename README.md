


# AWS S3 File Uploader and Downloader

## Overview

This Python project allows you to easily upload files to an AWS S3 bucket or specific folder and download files from there. It uses the `boto3` library for AWS interactions, `argparse` for command-line argument parsing.The project's environment and dependencies are managed using `Poetry`. All project dependencies and requirements are listed in the `pyproject.toml` file. You can manage and install these dependencies using Poetry, my preferred package and environment manager."

## Prerequisites

Before using this tool, make sure you have the following prerequisites installed:

- Python 3.11
- [Poetry](https://python-poetry.org/): You can install it following the [Poetry installation guide](https://python-poetry.org/docs/#installation).
- All dependencies can be installed using poetry. Simply run `poetry install` command.


## Configuration
### `.env` File

To configure this project, you'll need to create a `.env` file in the project directory. This file should contain the following keys, each with its corresponding value:

- `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.
- `BUCKET_NAME`: The name of your AWS S3 bucket.
- `BUCKET_FOLDER_IMAGES`: The folder path within the bucket where image files will be stored.
- `BUCKET_FOLDER_ANNOTATIONS`: The folder path within the bucket where annotation files will be stored.
## How to use
### Uploading Files
To upload a file to your AWS S3 bucket or folder, use the following command: 
`poetry run python3 Upload_to_AWS.py --bucket_name --s3_client --file_path --bucket_folder --object_name --file_type`

- `--bucket_name`: The s3 bucket bucket_name
- `--file_path`: Path of the file to be uploaded
- `--bucket_folder`: The name of the folder in the bucket
- `--object_name`: The name of the file in the bucket
- `--file_type`: Type of the files to be uploaded 
### Downloading Files
To download a file from your AWS S3 bucket or folder, use the following command:
`poetry run python3 Download_from_AWS.py --bucket_name --bucket_folder_images --bucket_folder_annotations --save_dir_images --save_dir_annot`

- `--bucket_name`: The s3 bucket bucket_name
- `--bucket_folder_images`: image folder name in s3 bucket
- `--bucket_folder_annotations`: folder name of the annotation files 
- `--save_dir_images`: local directory path to save downloaded images 
- `--save_dir_annot`: local directory path to save downloaded annotations
## Technologies Used
**Language:**  Python 3

**Library:** Boto3


[![python](https://camo.githubusercontent.com/3cdf9577401a2c7dceac655bbd37fb2f3ee273a457bf1f2169c602fb80ca56f8/68747470733a2f2f666f7274686562616467652e636f6d2f696d616765732f6261646765732f6d6164652d776974682d707974686f6e2e737667)](https://www.python.org/)  


## Authors

- [@armanbabayan](https://github.com/armanbabayan)

