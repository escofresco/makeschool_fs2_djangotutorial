from django.test import TestCase
from django.urls import reverse
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

class QuestionViewTests(TestCase):

    @staticmethod
    def make_question(text, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=text,
                                        pub_date=time)

    def test_no_question(self):
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question(self):
        QuestionViewTests.make_question(text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        QuestionViewTests.make_question(text="Past question.", days=-30)
        QuestionViewTests.make_question(text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        QuestionViewTests.make_question(text="Past question 1.", days=-30)
        QuestionViewTests.make_question(text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
