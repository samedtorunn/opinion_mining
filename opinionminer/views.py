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

        # Create trend graph
        plt.switch_backend('Agg')
        plt.figure(figsize=(12, 6))

        # Define cool palette colors
        colors = ['dodgerblue', 'limegreen', 'tomato']


        # Plot trend lines with cool palette colors
        plt.plot(dates, positive_counts, label='Positive', color=colors[1])
        plt.plot(dates, neutral_counts, label='Neutral', color=colors[0])
        plt.plot(dates, negative_counts, label='Negative', color=colors[2])

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
        wordcloud = WordCloud(width=1200, height=400, background_color='white').generate(text_data)



        wordcloud_path = 'opinionminer/static/opinionminer/wordcloud.png'
        wordcloud.to_file(wordcloud_path)

        return render(request, 'opinionminer/opinions.html', {
            'opinions': opinions,
            'topic': topic,
            'sentiment_distribution': sentiment_distribution,
            'trend_graph': graph_path
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
