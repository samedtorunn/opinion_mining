from django.shortcuts import render
import praw
from textblob import TextBlob
from .models import Opinion
from datetime import datetime
from langdetect import detect
import prawcore
import spacy

nlp = spacy.load('en_core_web_sm')

# Creative_Intern7785


reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret_key,
                     user_agent='My first App for Opinion Mining')

#This function below is not in use, get_sentiment_for_noun_phrases_array is used instead. To check the differencey
#between the scoring of the functions you can change the function calls in get_opinions
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        return 'positive'
    elif sentiment_score < 0:
        return 'negative'
    else:
        return 'neutral'


def get_sentiment_for_noun_phrases_array(noun_phrases):
        sentiment_scores = []
        for phrase in noun_phrases:
            blob = TextBlob(phrase)
            sentiment_score = blob.sentiment.polarity
            sentiment_subjectivity = blob.sentiment.subjectivity

            # To get more sharp results, subjectivity is increased.
            if sentiment_subjectivity >= 0.7:
                sentiment_scores.append(sentiment_score)

        # Calculate the overall sentiment based on the average score
        if len(sentiment_scores) == 0:
            average_score = 0;
        else:
            average_score = sum(sentiment_scores) / len(sentiment_scores)

        # Assign sentiment label based on the average score
        if average_score > 0:
            sentiment = 'positive'
        elif average_score < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return sentiment


# Since the accuracy of TextBlob is not satisfying after a few trials, I stopped using TextBlob, I started using
#Spacy. The function right below is not used anymore.
def extract_noun_phrases_with_TextBlob(text):
    blob = TextBlob(text)
    return blob.noun_phrases

def extract_noun_phrases(text):
    doc = nlp(text)
    noun_phrases = []
    for chunk in doc.noun_chunks:
        noun_phrases.append(chunk.text)
    return noun_phrases


def correct_spelling(text):
    text = TextBlob(text)
    corrected_text = text.correct()
    corrected_text = str(corrected_text)
    return corrected_text



def get_opinions(topic, start_date, end_date):
    opinions = []

    # Convert start_date and end_date to datetime objects
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    try:
        # Retrieve posts from the general Reddit search
        for submission in reddit.subreddit('all').search(topic, time_filter='all'):
            submission_time = datetime.fromtimestamp(submission.created_utc)
            if start_time <= submission_time <= end_time:
                lang = detect(submission.title + submission.selftext)
                if lang == 'en' and has_sentence(submission.selftext):
                    correct_spelling(submission.title)
                    correct_spelling(submission.selftext)
                    noun_phrases = extract_noun_phrases(submission.title + submission.selftext)
                    sentiment = get_sentiment_for_noun_phrases_array(noun_phrases)
                    print(submission.url)
                    opinion = Opinion(title=submission.title, text=submission.selftext,
                                      sentiment=sentiment, date=submission_time.date(), link=submission.url
                                      )
                    opinions.append(opinion)
    except prawcore.exceptions.Redirect:
        pass
    except prawcore.exceptions.NotFound:
        # Handle subreddit not found error
        return []

    # Remove spaces and convert to lowercase when checking for subreddit
    topic = topic.replace(" ", "").lower()

    if subreddit_exists(topic):
        try:
            # Retrieve posts from the specified subreddit
            for submission in reddit.subreddit(topic).search(topic, time_filter='all'):
                submission_time = datetime.fromtimestamp(submission.created_utc)
                if start_time <= submission_time <= end_time:
                    lang = detect(submission.title + submission.selftext)
                    if lang == 'en' and has_sentence(submission.selftext):
                        correct_spelling(submission.title)
                        correct_spelling(submission.selftext)
                        noun_phrases = extract_noun_phrases(submission.title + submission.selftext)
                        sentiment = get_sentiment_for_noun_phrases_array(noun_phrases)
                        opinion = Opinion(title=submission.title, text=submission.selftext,
                                          sentiment=sentiment, date=submission_time.date(),
                                          )
                        opinions.append(opinion)
        except prawcore.exceptions.Redirect:
            pass
        except prawcore.exceptions.NotFound:
            print("there is no subreddit on this topic.")
            pass

    return opinions


def subreddit_exists(subreddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except prawcore.exceptions.NotFound:
        exists = False
    return exists



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


def has_sentence(text):
    doc = nlp(text)
    return any(sent.text.strip() for sent in doc.sents)
