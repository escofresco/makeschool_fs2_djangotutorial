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
