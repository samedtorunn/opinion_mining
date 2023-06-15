from django.shortcuts import render, redirect
from .reddit_opinions import get_opinions, get_sentiment_distribution
from .forms import QueryForm
from .models import Opinion
from django.urls import reverse
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import sklearn
from sklearn.linear_model import LinearRegression
from wordcloud import STOPWORDS



def home_view(request):
    return render(request, 'opinionminer/home.html')


def opinions_view(request):
    form = QueryForm(request.GET or None)
    if form.is_valid():
        topic = form.cleaned_data['query']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        opinions = get_opinions(topic, start_date, end_date)

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
            datewise_opinions[opinion_date][sentiment] += 1

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
        plt.plot(dates, positive_counts, label='Positive', color=colors[1], linewidth=3)
        plt.plot(dates, neutral_counts, label='Neutral', color=colors[0], linewidth=3)
        plt.plot(dates, negative_counts, label='Negative', color=colors[2], linewidth=3)


        for sentiment, regression_line in regression_lines.items():
            y_pred = regression_line.predict(x)
            color = colors[1] if sentiment == 'positive' else colors[0] if sentiment == 'neutral' else colors[2]
            plt.plot(dates, y_pred, linestyle='dashed', label=f'{sentiment} regression line', color=color)

        # Customize the graph appearance
        plt.xlabel('Date')
        plt.ylabel('Opinion Count')
        plt.title('Daily Trends of Opinions')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Save the trend graph
        graph_path = 'opinionminer/static/opinionminer/trend_graph.png'
        plt.savefig(graph_path)
        plt.close()

        # Generate word cloud data
        text_data = ' '.join(opinion.text for opinion in opinions)
        excluded_words = set(STOPWORDS)  # Use the set of default STOPWORDS
        excluded_words.update(['https', 'www', 'com'])  # Add additional words to exclude
        wordcloud = WordCloud(width=1200, height=400, background_color='white', stopwords=excluded_words).generate(
            text_data)

        #wordcloud = WordCloud(width=1200, height=400, background_color='white').generate(text_data)

        # Save the word cloud image
        wordcloud_path = 'opinionminer/static/opinionminer/wordcloud.png'
        wordcloud.to_file(wordcloud_path)

        return render(request, 'opinionminer/opinions.html', {
            'opinions': opinions,
            'topic': topic,
            'sentiment_distribution': sentiment_distribution,
            'trend_graph': graph_path,
            'wordcloud': wordcloud_path
        })
    return redirect('home')



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

