
# from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .models import Message


def simple_view(request):
    return HttpResponse("<h1>simple view</h1>")


class MessageListView(ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['articleBody']

    def form_valid(self, form):
        form.instance.user = self.request.user.username
        return super(MessageCreateView, self).form_valid(form)


class MessageDetailView(DetailView):
    model = Message
    fields = ['articleBody']


class MeRedirectView(RedirectView):
    """ redirect /me to /@(request.user.username) """
    permanent = False

    def get_redirect_url(self):
        if self.request.user.is_authenticated():
            return reverse('message_user_list_view', args=[str(self.request.user.username)])
        else:
            return reverse('login')


class MessageUserListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super(MessageUserListView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']  # TODO clean?
        return context

    def get_queryset(self):
        return Message.objects.filter(user=self.kwargs['username'])


class HashtagListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super(HashtagListView, self).get_context_data(**kwargs)
        context['hashtag'] = self.kwargs['hashtag']
        return context

    def get_queryset(self):
        return Message.objects.filter(hashtags__name=self.kwargs['hashtag'])  # TODO: self.context?


class MessageUserHashtagListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super(MessageUserHashtagListView, self).get_context_data(**kwargs)
        context['hashtag'] = self.kwargs['hashtag']
        context['username'] = self.kwargs['username']
        return context

    def get_queryset(self):
        return Message.objects.filter(user=self.kwargs['username'])  # TODO: filter by hashtag
