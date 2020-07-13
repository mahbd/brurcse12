from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.shortcuts import render
from home.all_functions import a_update, c_update, d_update, country_translator, digit_translator, update, get_world
from .models import CoronaInfoC, CoronaInfoD, CoronaInfoA


def force_update(request):
    b = c_update()
    a = a_update()
    c = d_update()
    return HttpResponse(str(a[0]) + " Area " + str(b[0]) + " Country " + str(c[0]) + " District update failed<br>" +
                        str(a[1]) + " Area " + str(b[1]) + " Country " + str(c[1]) + " District update success")


def api(request):
    cnt_obj = CoronaInfoC.objects.all()
    dst_obj = CoronaInfoD.objects.all()
    area_obj = CoronaInfoA.objects.all()
    context = {
        'title': 'api',
        'cnt_obj': cnt_obj,
        'dst_obj': dst_obj,
        'area_obj': area_obj,
    }
    return render(request, 'home/api.html', context)


def country(request, name):
    try:
        cnt_obj = CoronaInfoC.objects.get(country=name)
    except CoronaInfoC.DoesNotExist:
        return HttpResponse("Wrong country name")
    except CoronaInfoC.MultipleObjectsReturned:
        return HttpResponse("Internal Error. Contact with administrator")
    res = {
        "set_attributes": {
            "country_name": country_translator(cnt_obj.country),
            "update_date": digit_translator(
                datetime.fromtimestamp(int(str(cnt_obj.updated)[0:10])).strftime("%d/%m/%Y %I:%M %p")),
            "total_cases": digit_translator(cnt_obj.cases),
            "total_deaths": digit_translator(cnt_obj.deaths),
            "total_recovered": digit_translator(cnt_obj.recovered),
            "new_cases": digit_translator(cnt_obj.todayCases),
            "new_recovered": digit_translator(cnt_obj.todayRecovered),
            "new_deaths": digit_translator(cnt_obj.todayDeaths),
            "death_per_million": digit_translator(cnt_obj.deathsPerOneMillion),
            "cases_per_million": digit_translator(cnt_obj.casesPerOneMillion),
            "recovered_per_million": digit_translator(cnt_obj.recoveredPerOneMillion),
            "sever_test": "1",
        }
    }
    try:
        return JsonResponse(res)
    finally:
        update('c')


def district(request, name):
    try:
        dis_obj = CoronaInfoD.objects.get(name=name)
    except CoronaInfoD.DoesNotExist:
        return HttpResponse("Wrong district name")
    except CoronaInfoD.MultipleObjectsReturned:
        return HttpResponse("Internal error. Contact administrator")
    res = {
        "set_attributes": {
            "district": dis_obj.bnName,
            "district_en": dis_obj.name,
            "confirmed": digit_translator(dis_obj.cases),
            "server_test": "1",
        }
    }
    try:
        return JsonResponse(res)
    finally:
        update('d')


def dhaka(request, name):
    try:
        dha_obj = CoronaInfoA.objects.get(name=name)
    except CoronaInfoA.DoesNotExist:
        return HttpResponse("Wrong area name")
    except CoronaInfoA.MultipleObjectsReturned:
        return HttpResponse("Internal error. Contact administrator")
    res = {
        "set_attributes": {
            "district": dha_obj.bnName,
            "district_en": dha_obj.name,
            "confirmed": digit_translator(dha_obj.cases),
            "server_test": "1",
        }
    }
    try:
        return JsonResponse(res)
    finally:
        update('a')


def world(request):
    res = get_world()
    return JsonResponse(res)
