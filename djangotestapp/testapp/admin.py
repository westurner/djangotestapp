from django.contrib import admin

import djangotestapp.testapp.models as models


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    fields = (
        'name',)
    readonly_fields = (
        'name',)
    list_display = (
        'name',)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateCreated'
    fields = (
        'articleBody',
        'user',
        'dateCreated',
        'likeCount',
        'hashtags',
        'users',
        'articleBody_html')
    readonly_fields = (
        'dateCreated',
        'likeCount',
        'hashtags',
        'users',
        'articleBody_html')
    list_display = (
        'articleBody',
        'user',
        'dateCreated')
