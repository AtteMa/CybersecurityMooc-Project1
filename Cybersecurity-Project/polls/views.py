from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from . import forms

from .models import Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def vote(request, question_id):
        # Here the SQL injection has been fixed using the django framework "models", which provides tools
        # for sanitizing the data in database queries. Using the models framework to execute database queries
        # prevents injection to the SQLite database.
        
        # One could execute the database queries directly. Here is an example of a direct database
        # connection with an injection:

        #   cursor = conn.cursor()
        #   cmd = """ UPDATE Choise SET (vote) WHERE id=(id) VALUES (?,?); """
        #   data = (selected_choise.votes, id)
        #   cursor.execute(cmd, data)
        #   conn.commit()

        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    def add_poll(request):
        # Here the SQL injection has been fixed using the django framework "models", which provides tools
        # for sanitizing the data in database queries. Using the models framework to execute database queries
        # prevents injection to the SQLite database.
        
        # One could execute the database queries directly. Here is an example of a direct database
        # connection with an injection:

        #   cursor = conn.cursor()
        #   cmd = """ INSERT INTO Question (question_text, pub_date) VALUES (?,?); """
        #   data = (question_text, pub_date)
        #   cursor.execute(cmd, data)
        #   conn.commit()

        if request.method == 'POST':
            form = forms.AddPoll(request.POST)
            formset = forms.QuestionMetaInlineFormset(request.POST)
            if form.is_valid() and formset.is_valid():
                currentForm = form.save(commit=False)
                currentForm.save()
                pollMetas = formset.save(commit=False)
                for meta in pollMetas:
                    meta.question = currentForm
                    meta.save()
                return redirect('polls:index')
        else:
            form = forms.AddPoll(initial={'pub_date': timezone.now()})
            product_meta_formset=forms.QuestionMetaInlineFormset()
        return render(request, 'polls/add_poll.html', {'form':form, 'product_meta_formset': product_meta_formset})