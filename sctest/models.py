from django.db import models

# Create your models here.


from django.db import models
from datetime import datetime


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name='学校名称')
    location = models.CharField(max_length=100, verbose_name='学校位置')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


class Student(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=20)
    age = models.IntegerField()


class StudentSorce(models.Model):
    student_id = models.IntegerField()
    math = models.FloatField()
    english = models.FloatField()
    chiness = models.FloatField()