"""Test cases for testing voting."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question, Choice

def create_question(question_text, days, end_days=30):
    """Create a question.

    Keyword arguments:
    question_text -- the question text
    days -- the days to add to now
    end_days -- the days to add to the publication date
    """
    date = datetime.timedelta(days=days)
    end_date = datetime.timedelta(days=end_days)
    time = timezone.now() + date
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time + end_date)


class UserVotingtests(TestCase):
    """Test class for voting."""

    def setUp(self):
        User.objects.create_user(username = 'jean', password = 'jeans123')

    def test_authenticated_user_vote(self):
        """Authenticated user try to vote a question."""
        self.new_question = create_question(question_text='How are you', days=-5)
        self.client.post(reverse('login'), {'username':'jean', 'password':'jeans123'}, follow = True)  
        url = reverse('polls:vote', args=(self.new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_vote(self):
        """Unauthenticated user try to vote a question."""
        self.new_question = create_question(question_text='How are you', days=-5)
        url = reverse('polls:vote', args=(self.new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
