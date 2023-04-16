from django.shortcuts import render
import praw
from textblob import TextBlob
from .models import Opinion


# Creative_Intern7785

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


def get_opinions(topic):

    opinions = []
    for submission in reddit.subreddit('all').search(topic):
        sentiment = get_sentiment(submission.title + submission.selftext)
        opinion = Opinion(title=submission.title, text=submission.selftext, sentiment=sentiment)
        opinions.append(opinion)
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




