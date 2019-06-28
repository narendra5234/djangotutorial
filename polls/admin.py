from django.contrib import admin

from django.contrib import admin

from .models import Question,Choice,Musician,Album,Person,Fruit,Person,Group,Membership,Ox,Person1
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
admin.site.register(Question,QuestionAdmin)
admin.site.register(Musician)
admin.site.register(Album)
admin.site.register(Person)
admin.site.register(Fruit)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Ox)
admin.site.register(Person1)

# Register your models here.
