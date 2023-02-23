from django.db import models
import json

# Create your models here.


class CounterfactualExplanation(models.Model):
    id = models.CharField(max_length=200)
    question = models.CharField(max_length=200)
    explanation = models.CharField(max_length=200)
