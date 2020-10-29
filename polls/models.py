"""Models class for database."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question class for model."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        """Return the question's text."""
        return self.question_text

    def was_published_recently(self):
        """Return if the question is recently published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return if the question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return true if question can vote."""
        return self.is_published() and (self.end_date > timezone.now())
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Choice class for model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice's text."""
        return self.choice_text

class Vote(models.Model):
    """Vote class for model."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default = None)
