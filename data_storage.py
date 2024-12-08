import boto3
import os
import json

def load_config(config_file="configs.json"):
    """
    Loads configuration values from a JSON file.
    """
    print("Loading configuration...")
    with open(config_file, "r") as f:
        config = json.load(f)
    print("Configuration loaded successfully.")
    return config

def upload_to_s3(local_path, bucket_name, s3_folder, aws_access_key, aws_secret_key, region):
    """
    Uploads local processed data to an S3 bucket.
    """
    print(f"Initializing S3 client in region {region}...")
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    print("S3 client initialized successfully.")

    # Iterate through JSON files in the local directory
    print(f"Uploading files from {local_path} to S3 bucket '{bucket_name}' in folder '{s3_folder}'...")
    for file in os.listdir(local_path):
        if file.endswith(".json"):
            local_file_path = os.path.join(local_path, file)
            s3_file_path = f"{s3_folder}/{file}"
            try:
                s3.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"Uploaded {file} to S3 at {s3_file_path}.")
            except Exception as e:
                print(f"Failed to upload {file}: {str(e)}")

    # Create a success file after uploading
    success_file_path = os.path.join(current_directory, "s3_upload_success.txt")
    with open(success_file_path, "w") as f:
        f.write("File upload completed successfully.")
    print("File upload completed.")

if __name__ == "__main__":
    try:
        # Load configuration
        config = load_config()

        # Define the local path for processed files and S3 parameters
        current_directory = os.path.dirname(os.path.abspath(__file__))
        local_data_path = os.path.join(current_directory, "processed_tweets")
        s3_bucket = config["S3_BUCKET"]
        s3_folder = config["S3_FOLDER"]
        aws_access_key = config["AWS_ACCESS_KEY_ID"]
        aws_secret_key = config["AWS_SECRET_ACCESS_KEY"]
        aws_region = config["AWS_REGION"]

        # Verify if the local path exists and contains files
        if not os.path.exists(local_data_path) or not os.listdir(local_data_path):
            print(f"No files found in directory: {local_data_path}")
        else:
            # Upload files to S3
            upload_to_s3(local_data_path, s3_bucket, s3_folder, aws_access_key, aws_secret_key, aws_region)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
