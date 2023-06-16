from django.test import TestCase
from datetime import datetime
from django.urls import reverse
from datetime import date
from .models import Opinion
from .reddit_opinions import get_opinions, get_sentiment_distribution
from .forms import QueryForm
from django.test import RequestFactory
from django.urls import reverse
from .views import home_view, opinions_view
from textblob import TextBlob
from .reddit_opinions import extract_noun_phrases, correct_spelling


class TextProcessingTestCase(TestCase):

    def test_correct_spelling(self):
        text = "Google is a good compny and alays value ttheir employees. 🍕"
        expected_corrected_text = "Google is a good company and always value their employees.🍕"

        result = correct_spelling(text)



class OpinionTestCase(TestCase):
    def test_get_opinions_from_future(self):
        # If the dates are in the future there should be no opinions.
        topic = "bitcoin"
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 7)


        opinions = get_opinions(topic, start_date, end_date)

        # Assert the test.
        self.assertEqual(len(opinions), 0)


    def test_get_opinions(self):
        #check if the function gets opinions
        topic = 'bitcoin'
        start_date = date(2023, 1, 1)
        end_date = date(2023, 4, 2)

        opinions = get_opinions(topic, start_date, end_date)

        self.assertIsInstance(opinions, list)
        self.assertGreaterEqual(len(opinions), 0)


    def test_get_opinions_with_more_than_one_keyword(self):
        #check if it works if a query has more than keywords,
        topic = 'Joe Biden'
        start_date = date(2023, 1, 1)
        end_date = date(2023, 4, 2)

        opinions = get_opinions(topic, start_date, end_date)

        self.assertIsInstance(opinions, list)
        self.assertGreaterEqual(len(opinions), 1)

    def test_opinions_view_no_opinions(self):
        # Test that opinions view handles no opinions found correctly
        topic = 'asadasdasdsafsadfsadasdsadasdewrwe'
        start_date = date.today()
        end_date = date.today()
        response = self.client.get(reverse('opinions'), {
            'query': topic,
            'start_date': start_date,
            'end_date': end_date,
        })
        self.assertTemplateUsed(response, 'opinionminer/error.html')

    def test_sentiment_distribution(self):
        # Ensure that the sentiment distribution function accurately counts sentiments
        from .reddit_opinions import get_sentiment_distribution

        opinions = [
            Opinion(sentiment='positive'),
            Opinion(sentiment='positive'),
            Opinion(sentiment='negative'),
            Opinion(sentiment='neutral'),
        ]

        distribution = get_sentiment_distribution(opinions)

        self.assertEqual(distribution['positive'], 2)
        self.assertEqual(distribution['negative'], 1)
        self.assertEqual(distribution['neutral'], 1)

    def test_get_sentiment(self):
        # Ensure that the sentiment function correctly identifies positive, negative, and neutral sentiments.
        from .reddit_opinions import get_sentiment

        positive_text = 'This is a wonderful experience'
        negative_text = 'This is a horrible experience'
        neutral_text = 'This is an experience'

        self.assertEqual(get_sentiment(positive_text), 'positive')
        self.assertEqual(get_sentiment(negative_text), 'negative')
        self.assertEqual(get_sentiment(neutral_text), 'neutral')
        print("Sentiments are right.")



class OpinionMinerTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view(self):
        request = self.factory.get(reverse('home'))
        response = home_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opinionminer/home.html')

    def test_opinions_view(self):
        request = self.factory.get(reverse('opinions'), {'query': 'test', 'start_date': '2022-01-01', 'end_date': '2022-01-02'})
        response = opinions_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opinionminer/opinions.html')
