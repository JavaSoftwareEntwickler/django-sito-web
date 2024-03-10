from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    
    titolo = models.CharField(max_length=50)
    descrizione = models.TextField(max_length=1000)
    data_ins = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)
    img = models.ImageField(upload_to='tasks/')
    def __str__(self):
        return f'{self.id} : {self.titolo}'

class Review(models.Model):
    reviewer_name = models.CharField(max_length=65)
    review_title =  models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
