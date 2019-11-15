from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Question

class QuestionModelTests(TestCase):

    def test_recently_published_future_question(self):
        """was_published_recently should return False for pub_date in the
        future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_recently_published_old_question(self):
        """was_published_recently should return False for pub_date older than
        a day"""
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_recently_published_recent_question(self):
        """was_published_recently should return True for pub_date a day old or
        newer"""
        time = timezone.now() - datetime.timedelta(seconds=23*60*60)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())
