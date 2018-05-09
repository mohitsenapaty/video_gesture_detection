# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseRedirect
import json, matplotlib, time
import matplotlib.pyplot as plt
import datetime as dt
from pytz import timezone 
from . import send_email
import dateutil.parser


# Create your views here.

def home(request):
    context = locals()
    template = 'home.html'
    returnDict = {} 
    return render(request, template, returnDict) 


def video_gesture_pre(request):
    template = 'video_gesture_pre.html'
    returnDict = {}
    return render(request, template, returnDict)

