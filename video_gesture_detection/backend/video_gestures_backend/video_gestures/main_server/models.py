# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class GestureMetric(models.Model):
    source          = models.TextField(primary_key=True)
    source_id       = models.TextField()
    attention_stat  = models.IntegerField(default=100)
    emotional_stat  = models.TextField()
    time_counter    = models.IntegerField(default=1)
    yawn_count      = models.IntegerField(default=1)

