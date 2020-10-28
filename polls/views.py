"""View function and class for polls."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Index view that show question list."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())

def poll_view(request, pk):
    """Show the detail of the question or error when vote is not allowed."""
    question = get_object_or_404(Question, pk=pk)
    previous_vote = False
    if Vote.objects.filter(user = request.user):
        previous_vote = Vote.objects.filter(user = request.user).first().choice.choice_text
    if not question.can_vote():
        messages.error(request, "Voting is not allowed! D:")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question, 'previous_vote': previous_vote})


class ResultsView(generic.DetailView):
    """Results view that show the result of the question."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """View for when user pressed vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user = request.user, question = question, defaults= {'choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(choice=choice).count()
            choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
