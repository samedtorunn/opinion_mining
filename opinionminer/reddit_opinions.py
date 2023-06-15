from django.shortcuts import render
import praw
from textblob import TextBlob
from .models import Opinion
from datetime import datetime, timedelta
from langdetect import detect
import prawcore


# Creative_Intern7785
secret_key = "GifgZ1mzRY82gHodCoJU-NYDhQBuOQ"
client_id = "d6A-_nqpbKUnJU9E5jYpWQ"


reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret_key,
                     user_agent='My first App for Opinion Mining')


def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        return 'positive'
    elif sentiment_score < 0:
        return 'negative'
    else:
        return 'neutral'


def get_opinions(topic, start_date, end_date):
    opinions = []

    # Convert start_date and end_date to datetime objects
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    # Remove spaces and convert to lowercase
    topic = topic.replace(" ", "").lower()

    try:
        # Retrieve posts from the general Reddit search
        for submission in reddit.subreddit('all').search(topic, time_filter='all'):
            submission_time = datetime.fromtimestamp(submission.created_utc)
            if start_time <= submission_time <= end_time:
                lang = detect(submission.title + submission.selftext)
                if lang == 'en':
                    sentiment = get_sentiment(submission.title + submission.selftext)
                    opinion = Opinion(title=submission.title, text=submission.selftext,
                                      sentiment=sentiment, date=submission_time.date())
                    opinions.append(opinion)
    except prawcore.exceptions.Redirect:
        pass

    try:
        # Retrieve posts from the specified subreddit
        for submission in reddit.subreddit(topic).search(topic, time_filter='all'):
            submission_time = datetime.fromtimestamp(submission.created_utc)
            if start_time <= submission_time <= end_time:
                lang = detect(submission.title + submission.selftext)
                if lang == 'en':
                    sentiment = get_sentiment(submission.title + submission.selftext)
                    opinion = Opinion(title=submission.title, text=submission.selftext,
                                      sentiment=sentiment, date=submission_time.date())
                    opinions.append(opinion)
    except prawcore.exceptions.Redirect:
        pass

    return opinions


def get_sentiment_distribution(opinions):
    distribution = {
        'positive': 0,
        'neutral': 0,
        'negative': 0,
    }
    for opinion in opinions:
        if opinion.sentiment == 'positive':
            distribution['positive'] += 1
        elif opinion.sentiment == 'neutral':
            distribution['neutral'] += 1
        elif opinion.sentiment == 'negative':
            distribution['negative'] += 1
    return distribution
