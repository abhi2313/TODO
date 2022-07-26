# from tkinter import CASCADE
from django.db import models
from sqlalchemy import true
from django.contrib.auth.models import User
# Create your models here.
# title,status,date,user,priority


class TODO(models.Model):
    status_choices = {
        ('C', 'Completed'),
        ('P', 'Pending'),
    }
    priority_choices={
        ('1','1️⃣'),
        ('2','2️⃣'),
        ('3','3️⃣'),
        ('4','4️⃣'),
        ('5','5️⃣'),
        
    }

    title = models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=2,choices=status_choices)
    date=models.DateTimeField(auto_now_add=True)
    priority=models.CharField(max_length=2,choices=priority_choices)

