from django.contrib import admin
from .models import Speurtocht, Question, GelopenTocht, Vraag, Player


class SpeurtochtAdmin(admin.ModelAdmin):
    list_display=('id', 'stad', 'description', 'is_active', 'no_of_questions', 'total_distance')

class QuestionAdmin(admin.ModelAdmin):
    list_display=('id', 'speurtocht', 'number', 'title')    
  
class PlayerAdmin(admin.ModelAdmin):
    list_display=('name', 'email') 

class VraagAdmin(admin.ModelAdmin):
    list_display=('question', 'number', 'answered', 'answer_correct', 'gt_code')    

class GelopenTochtAdmin(admin.ModelAdmin):
    list_display=('speurtocht', 'player', 'gt_code')


admin.site.register(Speurtocht, SpeurtochtAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Vraag, VraagAdmin)
admin.site.register(GelopenTocht, GelopenTochtAdmin)