from django.contrib import admin

import djangotestapp.tagbrowser.models as models


@admin.register(models.ResourceEdgeType)
class ResourceEdgeTypeAdmin(admin.ModelAdmin):
    fields = (
        'name',)
    readonly_fields = (
        'dateCreated',
        'dateModified')
    list_display = (
        'name',)


@admin.register(models.ResourceEdge)
class ResourceEdgeAdmin(admin.ModelAdmin):
    fields = (
        'type',
        'source',
        'dest',
        'user',
        'group',
        'data'
    )
    readonly_fields = (
        'dateCreated',
        'dateModified',
    )
    list_display = (
        'id',
        # 'type',   # ManyToMany
        # 'source', # ManyToMany
        # 'dest',   # ManyToMany
    )


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    fields = (
        'url',
        'name',)
    readonly_fields = (
        'data',)
    list_display = (
        'url', 'name',)


