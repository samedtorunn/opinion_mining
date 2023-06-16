from django.shortcuts import render, redirect
from .reddit_opinions import get_opinions, get_sentiment_distribution
from .forms import QueryForm
from .models import Opinion
from django.urls import reverse
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import sklearn
from sklearn.linear_model import LinearRegression
from wordcloud import STOPWORDS
from uuid import uuid4


def home_view(request):
    return render(request, 'opinionminer/home.html')

def about_view(request):
    return render(request, 'opinionminer/about.html')


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


def analyze_opinions(topic: str, opinions: list[Opinion], start_date, end_date):
    sentiment_distribution = get_sentiment_distribution(opinions)

    # Calculate daily trends
    datewise_opinions = {}
    current_date = start_date
    while current_date <= end_date:
        datewise_opinions[current_date] = {
            'positive': 0,
            'neutral': 0,
            'negative': 0
        }
        current_date += timedelta(days=1)

    for opinion in opinions:
        opinion_date = opinion.date
        sentiment = opinion.sentiment
        link = opinion.link
        datewise_opinions[opinion_date][sentiment] += 1

    trend_graph, wordcloud_path = create_and_save_graphs(topic, opinions, datewise_opinions, start_date, end_date)

    return {
        'opinions': opinions,
        'topic': topic,
        'sentiment_distribution': sentiment_distribution,
        'trend_graph': trend_graph,
        'wordcloud_path': wordcloud_path,
        'start_date': start_date,
        'end_date': end_date,
        'link': link
    }


def opinions_view(request):
    form = QueryForm(request.GET or None)
    if not form.is_valid():
        print(form.errors)
        return redirect('home')


    comparison_made = False
    topic = form.cleaned_data['query']
    compare_to = form.cleaned_data.get("compare_to")

    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']
    opinions = get_opinions(topic, start_date, end_date)


    # First we check if there are any opinions or not.
    if len(opinions) == 0:
        return render(request, 'opinionminer/error.html', {'message': 'No opinions found.'})
    else:
        results = [analyze_opinions(topic, opinions, start_date, end_date)]

        if compare_to:
            compare_to_opinions = get_opinions(compare_to, start_date, end_date)
            if compare_to_opinions:
                results.append(analyze_opinions(compare_to, compare_to_opinions, start_date, end_date))
                comparison_made = True
            else:
                return render(request, 'opinionminer/error.html', {'message': f'No opinions found for comparison topic {compare_to}.'})

        return render(request, 'opinionminer/opinions.html', {
            'primary_topic': topic,
            'results': results,
            'comparison_made': comparison_made,
        })


def create_and_save_graphs(topic: str, opinions: list[Opinion], datewise_opinions, start_date, end_date):
    # Prepare data for trend graph
    dates = list(datewise_opinions.keys())
    positive_counts = [datewise_opinions[date]['positive'] for date in dates]
    neutral_counts = [datewise_opinions[date]['neutral'] for date in dates]
    negative_counts = [datewise_opinions[date]['negative'] for date in dates]

    # Calculate linear regression lines
    x = np.arange(len(dates)).reshape(-1, 1)
    regression_lines = {
        'positive': LinearRegression().fit(x, positive_counts),
        'neutral': LinearRegression().fit(x, neutral_counts),
        'negative': LinearRegression().fit(x, negative_counts)
    }

    plt.switch_backend('Agg')
    plt.figure(figsize=(12, 6))

    # Define colors
    colors = ['lightgray', 'green', 'red']

    # Plot trend lines
    plt.plot(dates, positive_counts, label='Positive', color=colors[1], linewidth=2)
    plt.plot(dates, neutral_counts, label='Neutral', color=colors[0], linewidth=1)
    plt.plot(dates, negative_counts, label='Negative', color=colors[2], linewidth=2)

    for sentiment, regression_line in regression_lines.items():
        y_pred = regression_line.predict(x)
        color = colors[1] if sentiment == 'positive' else colors[0] if sentiment == 'neutral' else colors[2]
        plt.plot(dates, y_pred, linestyle='dashed', label=f'{sentiment} regression line', color=color)

    # Customize the graph appearance
    plt.xlabel('Date')
    plt.ylabel(f'{topic.title()} Opinion Count')
    plt.title(f'Daily Trends of Opinions on {topic.title()}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the trend graph
    trend_graph = f'/static/opinionminer/trend_graph-{uuid4()}.png'
    plt.savefig('opinionminer' + trend_graph)
    plt.close()

    # Generate word cloud data
    text_data = ' '.join(opinion.text for opinion in opinions)
    excluded_words = set(STOPWORDS)  # Use the set of default STOPWORDS
    excluded_words.update(['https', 'www', 'com'])  # Add additional words to exclude
    wordcloud = WordCloud(width=1200, height=400, background_color='white', stopwords=excluded_words).generate(
        text_data)

    # Save the word cloud image
    wordcloud_path = f'/static/opinionminer/wordcloud-{uuid4()}.png'
    wordcloud.to_file('opinionminer' + wordcloud_path)

    return trend_graph, wordcloud_path



