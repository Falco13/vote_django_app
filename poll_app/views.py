from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from poll_app.forms import CommentForm
from poll_app.models import Question, Vote, IpModel
from django.contrib.messages.views import SuccessMessageMixin
from poll_app.utils import can_change_vote


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HomeView(generic.ListView):
    template_name = 'poll_app/home.html'
    context_object_name = 'question_list'
    queryset = Question.objects.filter(is_active=True)


def detail_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    if request.user.is_authenticated:
        if Vote.objects.filter(voter=request.user, question=question).exists():
            messages.error(request, "Already Voted on this choice")
            return render(request, 'poll_app/detail.html', context={'question': question})
        else:
            return render(request, 'poll_app/detail.html', context={'question': question})
    else:
        return HttpResponseRedirect(reverse('poll_app:results', args=(slug,)))


class ResultsView(SuccessMessageMixin, generic.edit.FormMixin, generic.DetailView):
    model = Question
    template_name = 'poll_app/results.html'
    form_class = CommentForm
    success_message = 'Thank you for your comment!'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        ip = get_client_ip(self.request)

        if IpModel.objects.filter(ip=ip).exists():
            self.object.views.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            self.object.views.add(IpModel.objects.get(ip=ip))
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('poll_app:results', kwargs={'slug': self.object.question_relation.slug})

    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs, comm=self.object.comments.filter(is_active=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_voted_choices = []

        if self.request.user.is_authenticated:
            user_voted_choices = self.object.choice_set.filter(vote__voter=self.request.user)
        context['user_voted_choices'] = user_voted_choices
        context['comm'] = self.object.comments.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question_relation = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class AboutView(generic.TemplateView):
    template_name = 'poll_app/about.html'


# def vote(request, slug):
#     question = get_object_or_404(Question, slug=slug)
#     selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     Vote.objects.create(voter=request.user, choice=selected_choice, question=question)
#     messages.success(request, "Thanks for your vote!")
#     return HttpResponseRedirect(reverse('poll_app:results', args=(slug,)))

@can_change_vote
def vote(request, slug):
    question = get_object_or_404(Question, slug=slug)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    existing_vote = Vote.objects.filter(voter=request.user, question=question)
    if existing_vote.exists():
        existing_vote.delete()
        messages.info(request, "Your previous vote has been updated!")
    Vote.objects.create(voter=request.user, choice=selected_choice, question=question)
    messages.success(request, "Thanks for your vote!")
    return HttpResponseRedirect(reverse('poll_app:results', args=(slug,)))
