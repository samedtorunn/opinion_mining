from django.shortcuts import render
import praw
from textblob import TextBlob
from datetime import datetime
from langdetect import detect
import prawcore
import re
import csv

from .reddit_opinions import reddit_opinions


def extract_noun_phrases(text):
    text = text.lower()  #lowering the text characters
    doc = nlp(text)
    noun_phrases = []
    for chunk in doc.noun_chunks:
        noun_phrases.append(chunk.text)
    return noun_phrases

test = "The big brown dog chased the cat."

print(extract_noun_phrases(test))


