
# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def simple_view(request):
    return HttpResponse("<h1>simple view</h1>")


from django.views.generic import ListView
from .models import Message


class MessageListView(ListView):
    model = Message
