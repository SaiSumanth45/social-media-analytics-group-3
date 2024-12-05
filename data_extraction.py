import tweepy
import json
import os

# Load configuration from configs.json
def load_config(config_file="configs.json"):
    """
    Loads the configuration from a JSON file.
    """
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_file} not found. Please ensure it exists.")
        raise
    except json.JSONDecodeError:
        print(f"Error: {config_file} contains invalid JSON.")
        raise

def fetch_tweets(config_file="configs.json"):
    """
    Fetches tweets from Twitter API based on a query and returns them as JSON.
    """
    # Load credentials and parameters from config
    config = load_config(config_file)
    try:
        query = config["QUERY"]
        max_tweets = config["MAX_TWEETS"]
        BEARER_TOKEN = config["BEARER_TOKEN"]
    except KeyError as e:
        print(f"Missing configuration key: {e}")
        raise

    # Initialize Tweepy client
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    try:
        # Fetch tweets
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max_tweets,
            tweet_fields=["created_at", "text", "public_metrics"]
        )
        if not tweets.data:
            print("No tweets found for the given query.")
            return []

        # Format the tweet data
        tweet_data = [
            {
                "id": t.id,
                "text": t.text,
                "created_at": t.created_at.isoformat(),
                "metrics": t.public_metrics
            }
            for t in tweets.data
        ]
        return tweet_data

    except tweepy.errors.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        raise

if __name__ == "__main__":
    try:
        # Fetch tweets using configuration values
        data = fetch_tweets()

        # Get the current directory where the script is running
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the path for the raw_tweets.json file in the same directory
        raw_tweets_path = os.path.join(current_directory, "raw_tweets.json")

        # Save to JSON file
        with open(raw_tweets_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Raw tweets saved to {raw_tweets_path}.")

    except Exception as e:
        print(f"An error occurred: {e}")
