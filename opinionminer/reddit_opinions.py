from django.shortcuts import render
import praw
from textblob import TextBlob
from .models import Opinion
from datetime import datetime
from langdetect import detect
import prawcore
import spacy
import re
import csv
from wordcloud import STOPWORDS


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


def get_sentiment_for_noun_phrases_array(noun_phrases, emoji_scores):
    #SUBJECTIVITY
    sentiment_scores = []
    for phrase in noun_phrases:
        blob = TextBlob(phrase)
        sentiment_score = blob.sentiment.polarity
        sentiment_subjectivity = blob.sentiment.subjectivity

        # To get more sharp results, subjectivity is increased.
        if sentiment_subjectivity >= 0.5:  # WHY 0.5 IS CHOSEN CAN BE EXPLAINED HERE. CONFIFURATIN MANAGEMENT TOOLS, CHECK HYDRA.
            sentiment_scores.append(sentiment_score)

    # Add emoji scores to the sentiment scores
    sentiment_scores.extend(emoji_scores)

    # Calculate the overall sentiment based on the average score
    if len(sentiment_scores) == 0:
        average_score = 0;
    else:
        average_score = sum(sentiment_scores) / len(sentiment_scores)

    # Assign sentiment label based on the average score
    if average_score > 0.05:
        sentiment = 'positive'
    elif average_score < -0.05:
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
    text = text.lower()  #lowering the text characters
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


def get_opinions(topic, start_date, end_date): ### CHECK THIS FUNCTION IF IT GETS ALL THE RELATED POSTS OR NOT. !!!
    opinions = []
    fetched_opinions = set()  # Set to store unique opinion identifiers

    # Convert start_date and end_date to datetime objects
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    try:
        # Retrieve posts from the general Reddit search
        for submission in reddit.subreddit('all').search(topic, time_filter='all'):
            #print(submission.title)
            submission_time = datetime.fromtimestamp(submission.created_utc)
            if start_time <= submission_time <= end_time:
                print(submission.title)
                lang = detect(submission.title + submission.selftext)
                if lang == 'en' and has_sentence(submission.selftext):  # --> if this is filtered out, the change is 13 from 9
                    opinion_id = submission.id  # Get unique identifier of the opinion
                    if opinion_id not in fetched_opinions:
                        fetched_opinions.add(opinion_id)  # Add opinion identifier to set
                        emoji_list = emoji_scoring(submission.title + submission.selftext)
                        correct_spelling(submission.title)
                        correct_spelling(submission.selftext)
                        noun_phrases = extract_noun_phrases(submission.title + submission.selftext)
                        sentiment = get_sentiment_for_noun_phrases_array(noun_phrases,
                                                                                                   emoji_list)
                        opinion = Opinion(title=submission.title, text=submission.selftext,
                                          sentiment=sentiment, date=submission_time.date(), link=submission.url,
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
                        opinion_id = submission.id  # Get unique identifier of the opinion
                        if opinion_id not in fetched_opinions:
                            fetched_opinions.add(opinion_id)  # Add opinion identifier to set
                            emoji_list = emoji_scoring(submission.title + submission.selftext)
                            correct_spelling(submission.title)
                            correct_spelling(submission.selftext)
                            noun_phrases = extract_noun_phrases(submission.title + submission.selftext)
                            sentiment = get_sentiment_for_noun_phrases_array(noun_phrases, emoji_list)
                            opinion = Opinion(title=submission.title, text=submission.selftext,
                                              sentiment=sentiment, date=submission_time.date()
                                              )
                            opinions.append(opinion)
        except prawcore.exceptions.Redirect:
            pass
        except prawcore.exceptions.NotFound:
            pass

    topic = topic.replace(" ", "_").lower()
    if subreddit_exists(topic):
        try:
            # Retrieve posts from the specified subreddit
            for submission in reddit.subreddit(topic).search(topic, time_filter='all'):
                submission_time = datetime.fromtimestamp(submission.created_utc)
                if start_time <= submission_time <= end_time:
                    lang = detect(submission.title + submission.selftext)
                    if lang == 'en' and has_sentence(submission.selftext):
                        opinion_id = submission.id  # Get unique identifier of the opinion
                        if opinion_id not in fetched_opinions:
                            fetched_opinions.add(opinion_id)  # Add opinion identifier to set
                            emoji_list = emoji_scoring(submission.title + submission.selftext)
                            correct_spelling(submission.title)
                            correct_spelling(submission.selftext)
                            noun_phrases = extract_noun_phrases(submission.title + submission.selftext)
                            sentiment = get_sentiment_for_noun_phrases_array(noun_phrases, emoji_list)
                            opinion = Opinion(title=submission.title, text=submission.selftext,
                                              sentiment=sentiment, date=submission_time.date()
                                              )
                            opinions.append(opinion)
        except prawcore.exceptions.Redirect:
            pass
        except prawcore.exceptions.NotFound:
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

def is_emoji(s):
    emojis = re.findall(r'[^\w\s,]', s)
    for emoji in emojis:
        if '\U0001F300' <= emoji <= '\U0001F5FF' or '\U0001F600' <= emoji <= '\U0001F64F' or '\U0001F680' <= emoji <= '\U0001F6FF' or '\U0001F700' <= emoji <= '\U0001F77F' or '\U0001F780' <= emoji <= '\U0001F7FF' or '\U0001F800' <= emoji <= '\U0001F8FF' or '\U0001F900' <= emoji <= '\U0001F9FF' or '\U0001FA00' <= emoji <= '\U0001FA6F' or '\U0001FA70' <= emoji <= '\U0001FAFF' or '\U00002702' <= emoji <= '\U000027B0' or '\U0001F1E6' <= emoji <= '\U0001F1FF':
            return True
    return False

emoji_sentiment_dict = {}

with open('opinionminer/Emoji_Sentiment_Data_v1.0.csv', newline='', encoding='utf-8') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        emoji = row['Emoji']
        positive = int(row['Positive'])
        negative = int(row['Negative'])
        neutral = int(row['Neutral'])
        sentiment_score = (positive - negative) / (positive + negative + neutral)
        emoji_sentiment_dict[emoji] = sentiment_score

def get_emojis(s):
    emojis = re.findall(r'[^\w\s,]', s)
    emoji_list = [emoji for emoji in emojis if '\U0001F300' <= emoji <= '\U0001F5FF' or '\U0001F600' <= emoji <= '\U0001F64F' or '\U0001F680' <= emoji <= '\U0001F6FF' or '\U0001F700' <= emoji <= '\U0001F77F' or '\U0001F780' <= emoji <= '\U0001F7FF' or '\U0001F800' <= emoji <= '\U0001F8FF' or '\U0001F900' <= emoji <= '\U0001F9FF' or '\U0001FA00' <= emoji <= '\U0001FA6F' or '\U0001FA70' <= emoji <= '\U0001FAFF' or '\U00002702' <= emoji <= '\U000027B0' or '\U0001F1E6' <= emoji <= '\U0001F1FF']
    return emoji_list


def get_emoji_sentiment(emojis):
    sentiment_scores = [emoji_sentiment_dict.get(emoji, 0) for emoji in emojis]
    filtered_scores = [score for score in sentiment_scores if score != 0] # the filter is applied since not all the emojis included in our Emoji Sentiment data
    return filtered_scores

def emoji_scoring(s):
    emojis = re.findall(r'[^\w\s,]', s)
    emoji_list = [emoji for emoji in emojis if '\U0001F300' <= emoji <= '\U0001F5FF' or '\U0001F600' <= emoji <= '\U0001F64F' or '\U0001F680' <= emoji <= '\U0001F6FF' or '\U0001F700' <= emoji <= '\U0001F77F' or '\U0001F780' <= emoji <= '\U0001F7FF' or '\U0001F800' <= emoji <= '\U0001F8FF' or '\U0001F900' <= emoji <= '\U0001F9FF' or '\U0001FA00' <= emoji <= '\U0001FA6F' or '\U0001FA70' <= emoji <= '\U0001FAFF' or '\U00002702' <= emoji <= '\U000027B0' or '\U0001F1E6' <= emoji <= '\U0001F1FF']
    return get_emoji_sentiment(emoji_list)


# This function is not in use since it may change the meaning of the noun phrases that includes a phrasal verb like "give up"
def remove_stopwords(noun_phrases):
    cleaned_phrases = []
    for phrase in noun_phrases:
        # Split the phrase into individual words
        words = phrase.split()
        # Remove stop words from the words list
        filtered_words = [word for word in words if word.lower() not in STOPWORDS]
        # Reconstruct the cleaned phrase
        cleaned_phrase = ' '.join(filtered_words)
        cleaned_phrases.append(cleaned_phrase)
    return cleaned_phrases