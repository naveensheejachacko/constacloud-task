from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    class_grade = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    subject1 = models.CharField(max_length=50)
    score1 = models.IntegerField()
    subject2 = models.CharField(max_length=50)
    score2 = models.IntegerField()
    subject3 = models.CharField(max_length=50)
    score3 = models.IntegerField()
    subject4 = models.CharField(max_length=50)
    score4 = models.IntegerField()
    subject5 = models.CharField(max_length=50)
    score5 = models.IntegerField()
    photo = models.ImageField(upload_to='photos/')

    class Meta:
        unique_together = ('roll_no', 'class_grade')