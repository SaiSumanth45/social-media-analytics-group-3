import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
from textblob import TextBlob

def compute_sentiment(text):
    """
    Computes sentiment polarity of a text using TextBlob.
    """
    return TextBlob(text).sentiment.polarity if text else 0.0

def process_batches(input_path, output_path):
    """
    Processes cleaned data to calculate sentiment and save results.
    """
    spark = SparkSession.builder \
        .appName("BatchProcessing") \
        .config("spark.local.dir", "C:/Users/kanig/AppData/Local/Temp") \
        .getOrCreate()
    print(f"Python version used by PySpark: {spark.sparkContext.pythonExec}")

    # Load data
    df = spark.read.json(input_path)

    # Add sentiment score
    sentiment_udf = udf(compute_sentiment, DoubleType())
    df = df.withColumn("sentiment_score", sentiment_udf(df.cleaned_text))

    # Save processed data
    df.write.mode("overwrite").json(output_path)
    print(f"Processed data saved to {output_path}.")

if __name__ == "__main__":
    # Dynamically determine paths based on the script's location
    current_directory = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_directory, "cleaned_tweets")
    output_path = os.path.join(current_directory, "processed_tweets")
    
    # Call the function with dynamically determined paths
    process_batches(input_path, output_path)