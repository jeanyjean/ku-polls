"""Test cases for testing Detail page."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question

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

class QuestionDetailViewTests(TestCase):
    """Test class for QuestionDetail page."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns to the index page."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        User.objects.create_user(username = 'jean', password = 'jeans123')
        self.client.post(reverse('login'), {'username':'jean', 'password':'jeans123'}, follow = True)   
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
