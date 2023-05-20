from django.shortcuts import render, redirect
from .reddit_opinions import get_opinions, get_sentiment_distribution
from .forms import QueryForm
from .models import Opinion
from django.urls import reverse


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
        return render(request, 'opinionminer/opinions.html', {'opinions': opinions, 'topic': topic, 'sentiment_distribution': sentiment_distribution})
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
