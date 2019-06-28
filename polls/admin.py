from django.contrib import admin

from django.contrib import admin

from .models import Question,Choice
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)

# Register your models here.
