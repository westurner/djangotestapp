from django.contrib import admin

import djangotestapp.testapp.models as models


class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Message, MessageAdmin)
