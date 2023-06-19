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

