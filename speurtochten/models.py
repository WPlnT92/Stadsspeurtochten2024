from django.db import models
from django.urls import reverse


class Speurtocht(models.Model):
    stad = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    no_of_questions = models.IntegerField(null=True, blank=True)
    total_distance = models.FloatField(null=True, blank=True)
    img_1 = models.CharField(blank=True, null=True, max_length=254)
    img_2 = models.CharField(blank=True, null=True, max_length=254)
    price = models.CharField(max_length=8, blank=True, null=True)
    no_of_start_points = models.IntegerField(null=True, blank=True)
    descr_start_points = models.TextField(null=True, blank=True)
    start_point_map = models.CharField(blank=True, null=True, max_length=254)

    def get_absolute_url(self):
        return reverse('speurtocht', args=[str(self.stad)])

    def __str__(self):
        return self.stad    


class Question(models.Model):
    speurtocht = models.ForeignKey(Speurtocht, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)    
    possible_answer_1 = models.CharField(max_length=254, null=True, blank=True)
    possible_answer_2 = models.CharField(max_length=254, null=True, blank=True)
    possible_answer_3 = models.CharField(max_length=254, null=True, blank=True)
    possible_answer_4 = models.CharField(max_length=254, null=True, blank=True)
    correct_answer = models.IntegerField(null=True, blank=True)
    correct_answer_text = models.CharField(max_length=254, null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)
    next_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    map_coords = models.CharField(max_length=254, null=True, blank=True)
    marker = models.CharField(max_length=100, null=True, blank=True)
    route = models.TextField(blank=True)
    starting_point = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('question', args=[str(self.pk)])
    

class Player(models.Model):
    name = models.CharField(max_length=40, default="Speurder")
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class GelopenTocht(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True)
    speurtocht = models.ForeignKey(Speurtocht, on_delete=models.CASCADE)
    time_started = models.DateTimeField(blank=True, null=True)
    time_finished = models.DateTimeField(blank=True, null=True)
    first_question = models.IntegerField(blank=True, null=True)
    last_answered = models.IntegerField(blank=True, null=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    paid_for = models.BooleanField(default=False)
    gt_code = models.CharField(max_length=20, blank=True)
    overview = models.TextField(null=True, blank=True)
    payment_id = models.CharField(max_length=50, null=True, blank=True)


class Vraag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    number = models.IntegerField(null=True, blank=True) 
    answered = models.BooleanField(default=False)
    answer_correct = models.BooleanField(default=False)   
    gelopen_tocht = models.ForeignKey(GelopenTocht, on_delete=models.CASCADE) 
    gt_code = models.CharField(max_length=20, null=True)


class CodeTocht(models.Model):
    code_tocht = models.CharField(max_length=20, null=True, blank=True)	