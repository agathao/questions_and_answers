from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.core.mail import send_mail
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from forum.models import Answer, Question
from forum.forms import CreateQuestion, CreateAnswer

class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 1 

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

 
class Detail(generic.View):

    def get(self, request, *args, **kwargs):
        view = DetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DetailViewAddQuestion.as_view()
        return view(request, *args, **kwargs)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'forum/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = CreateAnswer()
        return context
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    

class DetailViewAddQuestion(SingleObjectMixin, FormView):
    template_name = 'forum/detail.html'
    form_class = CreateAnswer
    model = Question

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = CreateAnswer(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            answer = cd['answer']
            p = get_object_or_404(Question, pk=self.kwargs.get('pk', None))
            p.answer_set.create(answer_text=answer,creator=request.user)
        return super(DetailViewAddQuestion, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('forum:detail', kwargs={'pk': self.object.pk})
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'forum/results.html'

def user_login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/forum/')
            #TODO: ADD ERROR PAGES
    return render_to_response('forum/login.html', context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return render_to_response('forum/index.html', context_instance=RequestContext(request))

@login_required(login_url='/forum/login/')
def voteQuestionDown(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    p.votes += -1
    p.save()
    return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))
    
@login_required(login_url='/forum/login/')
def voteQuestionUp(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    p.votes += 1
    p.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))

@login_required(login_url='/forum/login/')
def voteDown(request, question_id, answer_id):
    vote(request, question_id, answer_id, -1)

@login_required(login_url='/forum/login/')
def voteUp(request, question_id, answer_id):
    vote(request, question_id, answer_id, 1)

def vote(request, question_id, answer_id, num):
    p = get_object_or_404(Question, pk=question_id)
    try:        
        selected_answer = p.answer_set.get(pk=answer_id)
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'forum/detail.html', {
            'question': p,
            'error_message': "You didn't select an answer.",
        })
    else:
        selected_answer.votes += num
        selected_answer.save()
        return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))
    
@login_required(login_url='/forum/login/')
def create_question(request):
    if request.method == 'POST':
        form = CreateQuestion(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            question = cd['question']
            tags = cd ['tags']
            q = Question(question_text=question, pub_date=timezone.now(), creator=request.user, tags_list=tags)
            q.save()
            
            for t in tags.split(','):
                q.tags_set.create(tag_text=t)
            
            return HttpResponseRedirect('/forum/')
    else:
        form = CreateQuestion()
    return render(request, 'forum/create_question.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/forum/login")
    else:
        form = UserCreationForm()
    return render(request, "forum/register.html", {
        'form': form,
    })
   
@login_required(login_url='/forum/login/')    
def edit_question(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    created_by = p.creator
    if created_by == request.user:
        if request.method == 'POST':
            form = CreateQuestion(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                question = cd['question']
                tags = cd ['tags']
                p.question_text = question
                p.mod_date = timezone.now()
                p.tags_list = tags
                p.save()
                return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))
        else:
            form = CreateQuestion(initial ={'question' : p.question_text, 'tags' : p.tags_list})
            return render(request, 'forum/edit.html', {'form': form, 'question': p})
    else:
        messages.add_message(request, messages.ERROR, "ERROR: You are not the creator of this question")
        return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))

@login_required(login_url='/forum/login/')    
def edit_answer(request, question_id, answer_id):
    p = get_object_or_404(Question, pk=question_id)
    try:        
        selected_answer = p.answer_set.get(pk=answer_id)
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'forum/detail.html', {
            'question': p,
            messages.ERROR: "You didn't select an answer.",
        })
    else:
        created_by = selected_answer.creator
        if created_by == request.user:
            if request.method == 'POST':
                form = CreateAnswer(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    answer = cd['answer']
                    selected_answer.answer_text = answer
                    selected_answer.mod_date = timezone.now()
                    selected_answer.save()
                    return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))
            else:
                form = CreateAnswer(initial ={'answer' : selected_answer.answer_text})
                return render(request, 'forum/edit.html', {'form': form, 'question': p, 'answer': selected_answer})
        else:
            messages.add_message(request, messages.ERROR, "ERROR: You are not the creator of this answer")
            return HttpResponseRedirect(reverse('forum:detail', args=(p.id,)))