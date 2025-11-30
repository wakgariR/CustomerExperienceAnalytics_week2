import pandas as pd
from tqdm import tqdm
# --- Sentiment Analysis Imports ---
# NOTE: The user MUST install the nltk library for VADER analysis:
# pip install nltk
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon if not present
try:
    # Check if the lexicon is already downloaded
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    # Download it if it's not found
    nltk.download('vader_lexicon', quiet=True)
# --- End Sentiment Analysis Imports ---


# --- Sentiment Analysis Function ---

def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes sentiment scores using VADER and classifies reviews into 
    Positive, Negative, or Neutral.
    
    NOTE: This uses VADER from the NLTK library (the simpler alternative).

    Args:
        df (pd.DataFrame): The DataFrame with a 'review' column.

    Returns:
        pd.DataFrame: The DataFrame with 'compound_score' and 'sentiment_label' columns.
    """
    # Sentiment analysis will now fail with ImportError if nltk or VADER is missing,
    # ensuring the packages are installed before proceeding.
    
    print("\n--- Starting Sentiment Analysis (using VADER) ---")
    sia = SentimentIntensityAnalyzer()

    # Calculate VADER sentiment scores for each review
    df['vader_scores'] = df['review'].apply(lambda review: sia.polarity_scores(str(review)))
    df['compound_score'] = df['vader_scores'].apply(lambda score: score['compound'])
    
    # Classify sentiment based on the compound score
    # These thresholds are standard for VADER:
    # Score >= 0.05 is positive, Score <= -0.05 is negative, otherwise neutral.
    def classify_sentiment(score):
        if score >= 0.05:
            return 'POSITIVE'
        elif score <= -0.05:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'

    df['sentiment_label'] = df['compound_score'].apply(classify_sentiment)
    
    print(f"Sentiment analysis complete. Added 'compound_score' and 'sentiment_label'.")
    return df.drop(columns=['vader_scores'], errors='ignore')


# --- Aggregation Function ---

def aggregate_sentiment(df: pd.DataFrame):
    """
    Aggregates sentiment results by bank and rating.

    Args:
        df (pd.DataFrame): The DataFrame with 'bank', 'rating', and sentiment columns.
    
    Returns:
        pd.DataFrame: Aggregated results showing mean compound score and sentiment counts.
    """
    if 'compound_score' not in df.columns:
        print("Skipping aggregation: Sentiment scores not available.")
        return None

    print("\n--- Starting Sentiment Aggregation ---")

    # 1. Mean Compound Score by Bank and Rating
    mean_sentiment = df.groupby(['bank', 'rating'])['compound_score'].mean().reset_index()
    mean_sentiment = mean_sentiment.rename(columns={'compound_score': 'mean_compound_score'})
    
    print("\nMean Compound Score per Bank and Rating:")
    print(mean_sentiment)

    # 2. Count of Sentiment Labels by Bank and Rating
    sentiment_counts = df.groupby(['bank', 'rating', 'sentiment_label']).size().reset_index(name='count')
    
    # Pivot the table to have sentiment labels as columns
    sentiment_pivot = sentiment_counts.pivot_table(
        index=['bank', 'rating'], 
        columns='sentiment_label', 
        values='count', 
        fill_value=0
    ).reset_index()
    
    # Ensure all labels are present, even if zero
    for label in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
        if label not in sentiment_pivot.columns:
            sentiment_pivot[label] = 0
            
    # Calculate the total reviews for percentage calculation
    sentiment_pivot['total_reviews'] = sentiment_pivot[['POSITIVE', 'NEGATIVE', 'NEUTRAL']].sum(axis=1)
    
    print("\nSentiment Label Counts per Bank and Rating:")
    print(sentiment_pivot)
    
    # Merge the mean score and counts into a final aggregate table
    final_aggregate = pd.merge(mean_sentiment, sentiment_pivot, on=['bank', 'rating'])
    
    print("\n--- Final Aggregated Results ---")
    print(final_aggregate)
    
    return final_aggregate