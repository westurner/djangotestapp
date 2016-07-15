from __future__ import unicode_literals

from django.db import models

class Message(models.Model):
    # user = models.ForeignKey('auth.models.User', default=current_user)
    user = models.TextField(db_index=True, max_length=42)
    message = models.TextField(db_index=True, max_length=140)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    starCount = models.IntegerField(default=0)