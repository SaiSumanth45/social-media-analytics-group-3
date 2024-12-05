import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace

def preprocess_data(input_path, output_path):
    """
    Cleans and preprocesses raw social media data.
    """
    spark = SparkSession.builder.appName("DataTransformation").getOrCreate()

    # Load data
    df = spark.read.option("multiline", "true").json(input_path)

    # Check if 'text' column exists
    if "text" not in df.columns:
        raise ValueError("Column 'text' not found in the input data.")

    # Clean text: lowercase and remove special characters
    df = df.withColumn("cleaned_text", lower(col("text")))
    df = df.withColumn("cleaned_text", regexp_replace(col("cleaned_text"), r"[^a-zA-Z\s]", ""))

    # Save cleaned data
    df.write.mode("overwrite").json(output_path)
    print(f"Cleaned data saved to {output_path}.")

if __name__ == "__main__":
    # Get the current directory where the script is running
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path for raw_tweets.json and cleaned_tweets.json in the same directory as the script
    raw_tweets_path = os.path.join(current_directory, "raw_tweets.json")
    cleaned_tweets_path = os.path.join(current_directory, "cleaned_tweets")
    
    # Call the preprocessing function with the dynamically determined paths
    preprocess_data(raw_tweets_path, cleaned_tweets_path)
