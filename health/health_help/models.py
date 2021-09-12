from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import PROTECT
from django.db.models.fields import CharField, CommaSeparatedIntegerField

class User(AbstractUser):
    pass

class Tablet(models.Model):
    username = models.ForeignKey(User , on_delete=PROTECT)
    tablet_name = models.CharField(max_length=250);
    time_taken = models.CharField(max_length=250);
    doseage = models.CharField(max_length=250 , blank=True);
    reason = models.CharField(max_length=350 , blank=True)
    doctor = models.CharField(max_length=350 , blank=True)

    def __str__(self):
        return f"{self.username} takes {self.tablet_name} at {self.time_taken}."

class Facts(models.Model):
    id = models.CharField(primary_key=True , max_length=100)
    fact = models.CharField(max_length=1500)

    def __str__(self):
        return f"{self.fact} - ({self.id})"


class Blogs(models.Model):
    user_name = models.CharField(max_length=200 ,  default='')
    unique_id = models.CharField(max_length=100 , unique=True)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=3500)
    image = models.URLField(max_length=500 , blank=True)

    def __str__(self):
        return f"Blog id is {self.unique_id}"

class Excercise(models.Model):
    id = models.CharField(primary_key=True , max_length=100)
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=1500)

    def __str__(self):
        return f"{self.title} - {self.id}"
    
class Recipies(models.Model):
    id = models.CharField(primary_key=True , max_length=100)
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=1500)
    calories = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.id}"


class Doctor(models.Model):
    username = models.CharField(max_length=500 , primary_key=True) 
    link = models.URLField(max_length=1500) 

    def __str__(self):
        return f"{self.username} - {self.link}"


class Comments(models.Model):
    link = models.ForeignKey(Doctor , on_delete=PROTECT)
    username = models.CharField(max_length=250 , default="")
    comments = models.CharField(max_length=250 , default="")
    comment_name = models.CharField(max_length=250 , default="")

    def __str__(self):
        return f"{self.comment_name} commented {self.comments}."

class Maps(models.Model):
    username = models.CharField(max_length=250 , default="")
    map_query = models.CharField(max_length=500 , default="")
    doctor_name = models.CharField(max_length=150 , default="")

    def __str__(self):
        return f"{self.map_query} - {self.doctor_name}"