from django.db import models
import json


class EcgReport(models.Model):
    atrial_fibrillation_flutter = models.CharField(max_length=200)
    avb = models.CharField(max_length=200)
    bigeminy = models.CharField(max_length=200)
    ear = models.CharField(max_length=200)
    ivr = models.CharField(max_length=200)
    junctional_rhythm = models.CharField(max_length=200)
    noise = models.CharField(max_length=200)
    sinus_rhythm = models.CharField(max_length=200)
    svt = models.CharField(max_length=200)
    trigeminy = models.CharField(max_length=200)
    ventricular_tachycardia = models.CharField(max_length=200)
    wenckebach = models.CharField(max_length=200)
    frequency_weighted_average = models.CharField(max_length=200)
