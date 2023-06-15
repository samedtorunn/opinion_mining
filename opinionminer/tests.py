from django.test import TestCase
from datetime import datetime, timedelta
from .reddit_opinions import get_opinions
from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Opinion
from .reddit_opinions import get_opinions, get_sentiment_distribution
from .forms import QueryForm


class OpinionTestCase(TestCase):
    def test_get_opinions_from_future(self):
        # If the dates are in the future there should be no opinions.
        topic = "bitcoin"
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 7)


        opinions = get_opinions(topic, start_date, end_date)

        # Assert the test.
        self.assertEqual(len(opinions), 0)  # Assuming there are no opinions in the specified date range


        def test_get_opinions(self):
            #check if the function gets opinions
            topic = 'bitcoin'
            start_date = date(2023, 1, 1)
            end_date = date(2023, 4, 2)

            opinions = get_opinions(topic, start_date, end_date)

            self.assertIsInstance(opinions, list)
            self.assertGreaterEqual(len(opinions), 0)
            for opinion in opinions:
                self.assertEqual(opinion.date, start_date)

        def test_get_opinions_with_more_than_one_keyword(self):
            #check if it works if a query has more than keywords,
            topic = 'Joe Biden'
            start_date = date(2023, 1, 1)
            end_date = date(2023, 4, 2)

            opinions = get_opinions(topic, start_date, end_date)

            self.assertIsInstance(opinions, list)
            self.assertGreaterEqual(len(opinions), 1)


