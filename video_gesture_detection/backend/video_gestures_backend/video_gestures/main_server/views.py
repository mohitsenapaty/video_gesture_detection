from __future__ import unicode_literals
import dateutil.parser
import json, matplotlib, time
import matplotlib.pyplot as plt
import datetime as dt
import redis

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from pytz import timezone
from video_gestures.main_server.models import GestureMetric
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



redisServer = redis.StrictRedis()
redisServer.set('gesture_result_count', str(0))
# Create your views here.

def home(request):
    context = locals()
    template = 'home.html'
    returnDict = {}
    return render(request, template, returnDict)

def get_emotional_index(row):
    source = row.source
    source_id = row.source_id
    emotional_stat 	= json.loads(row.emotional_stat)
    h, sr, sad, ang = [0 for x in range(4)]
    for item in emotional_stat:
        emotion = item["emotion"]
        value   = round(float(item["value"]), 3)
        if emotion == 'happy':
	        h = 2*value
        elif emotion == 'sad':
            sad = 0.7*value
        elif emotion == 'surprised':
            sr = value
        elif emotion == 'angry':
            ang = 0.3 * value
    attention 	= round(int(row.attention_stat)/100, 3)
    yawn_count 	= round(int(row.yawn_count)/2, 3)
    index 	= round((h+sr+sad+ang)/4, 3)
    index 	= index + attention - yawn_count
    return [source_id, index]


def recommendation_creation(request):
    all_rows = GestureMetric.objects.all()
    records = dict()
    for row in all_rows:
        sid, emotional_index = get_emotional_index(row)
        record = records.setdefault(sid, [])
        record.append(emotional_index)
    results = []
    for sid, indexes in records.items():
        avg_index = round(sum(indexes)/len(indexes), 3)
        results.append([sid, avg_index])
    results.sort(key=lambda x:x[1], reverse=True)
    return HttpResponse(json.dumps(results), content_type="application/json")


def get_stats(request):
    all_entries = GestureMetric.objects.all()
    new_count = all_entries.count()
    happy, sad, surprised, angry = [[] for x in range(4)]
    """count = redisServer.get('gesture_result_count')
    if not count:
        count = 0
        redisServer.set('gesture_result_count', str(count))
    if int(count) == new_count:
        result = dict(status='old_data')
        return HttpResponse(json.dumps(result), content_type="application/json")
    """
    #redisServer.set('gesture_result_count', str(new_count))
    attention_list = []
    for entries in all_entries:
        emotional_stat = json.loads(entries.emotional_stat)
        attention_list.append(entries.attention_stat)
        for item in emotional_stat:
            value = round(100*float(item["value"]))
            if item["emotion"] == 'happy':
                happy.append(value)
            elif item["emotion"] == 'sad':
                            sad.append(value)
            elif item["emotion"] == 'angry':
                            angry.append(value)
            elif item["emotion"] == 'surprised':
                            surprised.append(value)
    #result = dict(happy=happy[-10:], sad=sad[-10:], surprised=surprised[-10:], angry=angry[-10:])
    result = dict(happy=happy, sad=sad, surprised=surprised, angry=angry, attention_list=attention_list)
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def display_realtime_stats(request):
#return http and render the realtime data from js file.
    received_json_data=json.loads(request.body)
    attentionData   = received_json_data["attentionData"]
    emotionData     = received_json_data["emotionData"]
    youtube_id      = received_json_data["youtube_id"]
    numYawns        = received_json_data["numYawns"]
    time_counter    = received_json_data["time_counter"]
    yawn_count      = received_json_data["numYawns"]

    unique_id   = '_'.join([youtube_id, str(time_counter)])
    obj         = GestureMetric(source=unique_id, source_id=youtube_id,
                                time_counter=int(time_counter),
                                attention_stat=int(attentionData),
                                emotional_stat=json.dumps(emotionData),
                                yawn_count = int(yawn_count)
                                )
    obj.save()
    return HttpResponse('Success!!')


def get_attention_data(request):
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

