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

    def test_replace_user_vote(self):  
        self.new_question = create_question(question_text='How are you', days=-5)
        self.first_choice = Choice(id = 1, question = self.new_question, choice_text = "I'm ok")
        self.second_choice = Choice(id = 2, question = self.new_question, choice_text = "I'm fine")
        self.first_choice.save()
        self.second_choice.save()
        self.client.login(username='jean', password='jeans123')
        response = self.client.post(reverse('polls:vote', args=(self.new_question.id,)), {'choice':self.first_choice.id})
        self.first_choice = self.new_question.choice_set.get(pk = self.first_choice.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.first_choice.vote_set.all().count(), 1)
        response = self.client.post(reverse('polls:vote', args=(self.new_question.id,)), {'choice':self.second_choice.id})
        self.second_choice = self.new_question.choice_set.get(pk = self.second_choice.id)
        self.first_choice = self.new_question.choice_set.get(pk = self.first_choice.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.second_choice.vote_set.all().count(), 1)
        self.assertEqual(self.first_choice.vote_set.all().count(), 0)
    
    # def test_show_user_previous_vote(self):


