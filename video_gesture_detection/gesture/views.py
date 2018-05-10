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


def video_gesture_pre_no_outline(request):
    template = 'video_gesture_pre_no_outline.html'
    returnDict = {}
    return render(request, template, returnDict)


def video_gesture_pre_all(request):
    template = 'video_gesture_pre_all.html'
    returnDict = {}
    return render(request, template, returnDict)


def video_gesture_pre_all_no_outline(request):
    template = 'video_gesture_pre_all_no_outline.html'
    returnDict = {}
    return render(request, template, returnDict)


@csrf_exempt
def get_attention_data(request):
    #fromJs = json.loads(request.POST)
    #print fromJs
    #import pdb; pdb.set_trace();
    att_array = request.POST.getlist(u'colAttentionData[]')
    is_logged_in = 0
    _username = request.session.get("username", "")
    if not _username == "":
        #return HttpResponseRedirect('/combined_app/')
        is_logged_in = 1
        #_username = 
    float_att_array = []
    id_ = 0
    x_arr = []
    for att in att_array:
        float_att_array.append(float(att))
        id_ += 1
        x_arr.append(id_)
    plt.plot(x_arr, att_array)
    plt.xlabel("time in seconds")
    plt.ylabel("attention level in percent")
    plt_file_name = "attention_data_"
    dt_timestamp = dt.datetime.fromtimestamp(time.time()).strftime("%Y_%m_%d_%H_%M_%S")
    plt_file_name = _username + plt_file_name+dt_timestamp+".png"
    plt.savefig(plt_file_name)
    plt.gcf().clear()
    glob_att_file = plt_file_name
    glob_emo_file = request.session.get("glob_emo_file")
    if not glob_emo_file == None:
        del request.session["glob_emo_file"]
        request.session.modified = True
    send_email.send_email("date:val time:val", "dharna graph for user", [glob_att_file, glob_emo_file])
        #upload emotion file
    return HttpResponse("Success!")


@csrf_exempt
def get_emotion_data(request):
    #fromJs = json.loads(request.POST)
    #print fromJs
    #import pdb; pdb.set_trace();
    post_array = request.POST
    is_logged_in = 0
    _username = request.session.get("username", "")
    if not _username == "":
        #return HttpResponseRedirect('/combined_app/')
        is_logged_in = 1
    i_ = 0
    j_ = 0
    emo_dict = {"angry":[0], "sad":[0], "surprised":[0], "happy":[0]}
    while (1):
        flag = 0
        for j_ in range(4):
            qe_str = 'data['+str(i_)+"]["+str(j_)+"][emotion]"
            qv_str = 'data['+str(i_)+"]["+str(j_)+"][value]"
            emo_ = post_array.getlist(qe_str)
            val_ = post_array.getlist(qv_str)
            if emo_==None or len(emo_) == 0:
                flag = 1
                break
            else:
                emo_list = emo_dict.get(emo_[0])
                if emo_list == None or len(emo_list) == 0:
                    pass
                else:
                    emo_dict[emo_[0]].append(val_[0])

        i_ = i_+1
        if flag == 1:
            break

    #print emo_dict
    #float_emotion_array = []
    #id_ = 0
    #x_arr = []
    plot_key = []
    for emo_key in emo_dict:
        emo_arr = emo_dict[emo_key]
        p_key = "y = "+emo_key
        plot_key.append(emo_key)
        float_emo_arr = []
        x_arr = []
        id_ = 0
        for emo_val in emo_arr:
            float_emo_arr.append(float(emo_val))
            x_arr.append(id_)
            id_+=1
        plt.plot(x_arr, float_emo_arr)
    plt.legend(plot_key, loc='upper left')


    #    float_att_array.append(float(att))
    #    id_ += 1
    #    x_arr.append(id_)
    #plt.plot(x_arr, att_array)
    plt.xlabel("time in seconds")
    plt.ylabel("weighted emotion value")
    plt_file_name = "emotion_data_"
    dt_timestamp = dt.datetime.fromtimestamp(time.time()).strftime("%Y_%m_%d_%H_%M_%S")
    plt_file_name = _username + plt_file_name+dt_timestamp+".png"
    plt.savefig(plt_file_name)
    plt.gcf().clear()
    #global glob_emo_file
    request.session["glob_emo_file"] = plt_file_name
    return HttpResponse("Success!")

