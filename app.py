import streamlit as st
import json
import os
import subprocess
import logging

CONFIG_FILE = "configs.json"
LOG_FILE = "error_log.txt"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to save user inputs to configs.json
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    st.success(f"Configuration saved to {CONFIG_FILE}.")

# Function to load existing config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "QUERY": "",
            "MAX_TWEETS": 10,
            "BEARER_TOKEN": "",
            "S3_BUCKET": "",
            "S3_FOLDER": "",
            "AWS_ACCESS_KEY_ID": "",
            "AWS_SECRET_ACCESS_KEY": "",
            "AWS_REGION": "us-east-1",
        }

# Function to check if a file or folder exists and log error if not
def check_path_exists(path, step_name, is_folder=False):
    if (is_folder and os.path.isdir(path)) or (not is_folder and os.path.exists(path)):
        st.success(f"{step_name} completed successfully.")
    else:
        error_message = f"{step_name} failed: {path} not found."
        logging.error(error_message)
        st.error(error_message)
        st.stop()

# Load the existing configuration
config = load_config()

# Streamlit UI
st.title("Social Media Analytics Configuration")

st.header("Twitter API Settings")
query = st.text_input(
    "Query (e.g., Elon)",
    value=config.get("QUERY", ""),
    help="Enter the keyword or hashtag to search for."
)
max_tweets = st.number_input(
    "Max Tweets",
    min_value=1,
    value=config.get("MAX_TWEETS", 10),
    step=1,
    help="Enter the maximum number of tweets to fetch."
)
bearer_token = st.text_input(
    "Bearer Token",
    value=config.get("BEARER_TOKEN", ""),
    type="password",
    help="Twitter API Bearer Token."
)

st.header("AWS S3 Settings")
s3_bucket = st.text_input(
    "S3 Bucket Name",
    value=config.get("S3_BUCKET", ""),
    help="Name of the S3 bucket for storing processed tweets."
)
s3_folder = st.text_input(
    "S3 Folder Name",
    value=config.get("S3_FOLDER", ""),
    help="Folder in the S3 bucket to upload data."
)
aws_access_key_id = st.text_input(
    "AWS Access Key ID",
    value=config.get("AWS_ACCESS_KEY_ID", ""),
    type="password",
    help="AWS Access Key ID."
)
aws_secret_access_key = st.text_input(
    "AWS Secret Access Key",
    value=config.get("AWS_SECRET_ACCESS_KEY", ""),
    type="password",
    help="AWS Secret Access Key."
)
aws_region = st.text_input(
    "AWS Region",
    value=config.get("AWS_REGION", "us-east-1"),
    help="Region of your S3 bucket."
)

# Save inputs to config file
if st.button("Save Configuration"):
    updated_config = {
        "QUERY": query,
        "MAX_TWEETS": max_tweets,
        "BEARER_TOKEN": bearer_token,
        "S3_BUCKET": s3_bucket,
        "S3_FOLDER": s3_folder,
        "AWS_ACCESS_KEY_ID": aws_access_key_id,
        "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
        "AWS_REGION": aws_region,
    }
    save_config(updated_config)

# Run the pipeline
if st.button("Run Pipeline"):
    steps = [
        {"script": "data_extraction.py", "output": "raw_tweets.json", "step_name": "Data Extraction", "is_folder": False},
        {"script": "data_transformation.py", "output": "cleaned_tweets", "step_name": "Data Transformation", "is_folder": True},
        {"script": "batch_processing.py", "output": "processed_tweets", "step_name": "Batch Processing", "is_folder": True},
        {"script": "data_storage.py", "output": "s3_upload_success.txt", "step_name": "Data Storage", "is_folder": False},
    ]

    for step in steps:
        try:
            # Execute the script
            subprocess.run(["python", step["script"]], check=True)
            # Check if the output path exists
            check_path_exists(step["output"], step["step_name"], is_folder=step["is_folder"])
        except subprocess.CalledProcessError as e:
            # Log the error and display it in the UI
            error_message = f"Error in {step['step_name']} ({step['script']}): {e}"
            logging.error(error_message)
            st.error(error_message)
            st.stop()  # Halt further execution

    st.success("Pipeline executed successfully.")

st.title("Power BI Report in Streamlit")

# Power BI embed link (replace with your link)
embed_url = "https://app.powerbi.com/reportEmbed?reportId=505cd622-7df4-4329-bf18-9eca744f2daa&autoAuth=true&ctid=0d85160c-5899-44ca-acc8-db1501b993b6"

# Embed Power BI report
st.components.v1.iframe(embed_url, width=800, height=600)
