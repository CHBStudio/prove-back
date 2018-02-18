from django.contrib import admin

from landing.models import Faq, Result


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    fields = ('question', 'answer')


admin.site.register(Faq, FaqAdmin)
admin.site.register(Result)
