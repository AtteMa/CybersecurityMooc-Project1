from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Choice, Question
from . import forms


# Here we can add a logger to track for example voting and the addition of polls. This will make
# locating possible bugs or malicious activity much easier.

# import logger
# logger = logging.getLogger('pollsAppLogger')
# logger.debug("Hello, this is a logged text")

@csrf_exempt
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

@csrf_exempt
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

@csrf_exempt
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def vote(request, question_id):
        # Here the SQL injection has been fixed using the django framework "models", which provides tools
        # for sanitizing the data in database queries. Using the models framework to execute database queries
        # prevents injection to the SQLite database.
        
        # One could execute the database queries directly. Here is an example of a direct database
        # connection with an injection:
        
        #   choice = request.POST['choice']
        #   question_id = request.POST['question_id']
        #   cursor = conn.cursor()
        #   cursor.execute("UPDATE Choise SET (vote) WHERE id LIKE '%%%s%%' VALUES ('"+ choice +"', '"+ question_id +"');")
        #   conn.commit()

        
        # Here we could add a session check to see if a user has already voted on a question
        """
        if f'voted_{question_id}' in request.session:
            messages.error(request, "You have already voted for this question.")
            return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
        """

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

            #here we set the question as "voted"
            """request.session[f'voted_{question_id}'] = True"""

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    def add_poll(request):
        # Here the SQL injection has been fixed using the django framework "models", which provides tools
        # for sanitizing the data in database queries. Using the models framework to execute database queries
        # prevents injection to the SQLite database.
        
        # One could execute the database queries directly. Here is an example of a direct database
        # connection with an injection:

        #   question_text = request.POST['question_text']
        #   pub_date = request.POST['pub_date']
        #   cursor = conn.cursor()
        #   cmd = cursor.execute("INSERT INTO Question (question_text, pub_date) VALUES ('"+ question_text +"','"+ pub_date +"');")
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