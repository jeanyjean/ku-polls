"""Test cases for testing Models"""
import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question

class QuestionModelTests(TestCase):
    """Test class for the question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_old_question(self):
        """is_published() return True when the date is past the pub_date."""
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.is_published())

    def test_is_published_with_recent_question(self):
        """is_published() return True when the date is recently past the pub_date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.is_published())

    def test_is_published_with_future_question(self):
        """is_published() return False when the date is not past the pub_date yet."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_can_vote_with_question_past_end_date(self):
        """can_vote() return False when the date is past the pub_date and past the end_date."""
        pub_time = timezone.now() - datetime.timedelta(days=3)
        end_time = pub_time + datetime.timedelta(days=2)
        closed_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(closed_question.can_vote())

    def test_can_vote_with_question_within_end_date(self):
        """can_vote() return True when the date is past the pub_date and not past the end_date."""
        pub_time = timezone.now() - datetime.timedelta(days=5)
        end_time = pub_time + datetime.timedelta(days=10)
        opened_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertTrue(opened_question.can_vote())

    def test_can_vote_with_question_not_published(self):
        """can_vote() return False when question is not published yet."""
        pub_time = timezone.now() + datetime.timedelta(days=5)
        end_time = pub_time + datetime.timedelta(days=5)
        closed_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(closed_question.can_vote())
