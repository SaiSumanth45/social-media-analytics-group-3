import streamlit as st
import json
import os
import subprocess

CONFIG_FILE = "configs.json"

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

# Streamlit UI
st.title("Social Media Analytics Configuration")

st.header("Twitter API Settings")
query = st.text_input("Query (e.g., Elon)", help="Enter the keyword or hashtag to search for.")
max_tweets = st.number_input("Max Tweets", min_value=1, value=10, help="Maximum number of tweets to fetch.")
bearer_token = st.text_input("Bearer Token", type="password", help="Twitter API Bearer Token.")

st.header("AWS S3 Settings")
s3_bucket = st.text_input("S3 Bucket Name", help="Name of the S3 bucket for storing processed tweets.")
s3_folder = st.text_input("S3 Folder Name", help="Folder in the S3 bucket to upload data.")
aws_access_key_id = st.text_input("AWS Access Key ID", type="password", help="AWS Access Key ID.")
aws_secret_access_key = st.text_input("AWS Secret Access Key", type="password", help="AWS Secret Access Key.")
aws_region = st.text_input("AWS Region", value="us-east-1", help="Region of your S3 bucket.")

# Load the existing configuration
config = load_config()

# Populate fields with existing configuration
if st.button("Load Existing Configuration"):
    query = config.get("QUERY", "")
    max_tweets = config.get("MAX_TWEETS", 10)
    bearer_token = config.get("BEARER_TOKEN", "")
    s3_bucket = config.get("S3_BUCKET", "")
    s3_folder = config.get("S3_FOLDER", "")
    aws_access_key_id = config.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = config.get("AWS_SECRET_ACCESS_KEY", "")
    aws_region = config.get("AWS_REGION", "us-east-1")
    st.success("Configuration loaded successfully.")

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
    try:
        # Run each script sequentially
        subprocess.run(["python", "data_extraction.py"], check=True)
        subprocess.run(["python", "data_transformation.py"], check=True)
        subprocess.run(["python", "batch_processing.py"], check=True)
        subprocess.run(["python", "data_storage.py"], check=True)
        st.success("Pipeline executed successfully.")
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred while running the pipeline: {e}")
