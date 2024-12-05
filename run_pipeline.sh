#!/bin/bash

# Ensure the script is being executed from the directory where the Python scripts are located
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "$SCRIPT_DIR"

# Check if configs.json exists
if [[ ! -f "configs.json" ]]; then
    echo "Error: configs.json file is missing."
    exit 1
fi

# Check if the necessary Python environment is set up (e.g., pyspark, textblob, boto3, tweepy)
python -c "import pyspark, textblob, boto3, tweepy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Required Python packages (pyspark, textblob, boto3, tweepy) are not installed."
    exit 1
fi

# Step 1: Run the Python script for data extraction
echo "Running data extraction script..."
python data_extraction.py

# Check if data extraction was successful
if [ $? -eq 0 ]; then
    echo "Data extraction completed successfully."
else
    echo "Error: Data extraction failed."
    exit 1
fi

# Step 2: Run the Python script for data transformation (preprocessing)
echo "Running data preprocessing script..."
python data_transformation.py

# Check if data transformation was successful
if [ $? -eq 0 ]; then
    echo "Data preprocessing completed successfully."
else
    echo "Error: Data preprocessing failed."
    exit 1
fi

# Step 3: Run the Python script for sentiment analysis
echo "Running sentiment analysis script..."
python batch_processing.py

# Check if sentiment analysis was successful
if [ $? -eq 0 ]; then
    echo "Sentiment analysis completed successfully."
else
    echo "Error: Sentiment analysis failed."
    exit 1
fi

# Step 4: Run the Python script for uploading processed data to S3
echo "Running S3 upload script..."
python data_storage.py

# Check if S3 upload was successful
if [ $? -eq 0 ]; then
    echo "Data uploaded to S3 successfully."
else
    echo "Error: Data upload to S3 failed."
    exit 1
fi

echo "All processing steps completed successfully!"
