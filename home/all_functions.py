import random
import string
from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from api.models import CoronaInfoA, CoronaInfoD, CoronaInfoC
from home.models import UpdateTime

from chat.models import LastMessage


def get_name(user):
    try:
        name = user.userinfo.nick_name
    except:
        name = user.first_name + " " + user.last_name
    if name == ' ':
        return user.username
    return name


def get_name_by_id(user_id):
    user = User.objects.get(id=user_id)
    name = get_name(user)
    return name


def paging(request, all_obj, item_per_page=10):
    spl_obj = Paginator(all_obj, item_per_page)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1
    return spl_obj.get_page(page_num)


def make_read(request):
    last_messages_obj = LastMessage.objects.filter(recipient_id=request.user.id)
    for last_message in last_messages_obj:
        mes = LastMessage.objects.get(id=last_message.id)
        mes.read = True
        mes.save()


def mes_check(model, sender_id, recipient_id):
    return model.objects.filter(((models.Q(sender_id=sender_id) & models.Q(recipient_id=recipient_id)) | (
            models.Q(sender_id=recipient_id) & models.Q(recipient_id=sender_id))))


def last_message_update(user, recipient_id, message):
    if mes_check(LastMessage, user.id, recipient_id):
        try:
            last_obj = LastMessage.objects.get(
                (models.Q(recipient_id=user.id)) & models.Q(sender_id=recipient_id))
        except LastMessage.DoesNotExist:
            last_obj = LastMessage.objects.get(
                (models.Q(sender_id=user.id)) & models.Q(recipient_id=recipient_id))
        last_obj.sender = user
        last_obj.recipient_id = recipient_id
        last_obj.message = message
        last_obj.read = False
    else:
        last_obj = LastMessage(sender=user, recipient_id=recipient_id, message=message, read=False)
    last_obj.save()


def email_validation(user, email):
    if email == '':
        return user
    else:
        try:
            user_obj = User.objects.get(email=email)
            if user.id == user_obj.id:
                return user
            else:
                return user_obj
        except User.DoesNotExist:
            return user
        except User.MultipleObjectsReturned:
            return False


def token_generator(stl=8):
    lad = string.ascii_letters
    return ''.join((random.choice(lad) for _ in range(stl)))


def get_world():
    try:
        world_page = requests.get('https://disease.sh/v2/all?yesterday=false&allowNull=false').json()
    except:
        return {"server_test": 0}
    return {
        "update_date": digit_translator(
                datetime.fromtimestamp(int(str(world_page["updated"])[0:10])).strftime("%d/%m/%Y %I:%M %p")),
        "total_cases": digit_translator(world_page["cases"]),
        "total_death": digit_translator(world_page["deaths"]),
        "total_recovered": digit_translator(world_page["recovered"]),
    }


def d_update():
    try:
        all_dis = requests.get('https://covid19bangladesh.pythonanywhere.com/district').json()['features']
    except:
        return ["server is bad", 0]
    fails = 0
    success = 0
    for dis in all_dis:
        try:
            CoronaInfoD.objects.get_or_create(name=dis['properties']['name'])
            dis_obj = CoronaInfoD.objects.get(name=dis['properties']['name'])
            dis_obj.bnName = dis['properties']['bnName']
            dis_obj.cases = dis['properties']['confirmed']
            dis_obj.save()
            success += 1
        except:
            fails += 1
    return [fails, success]


def a_update():
    try:
        all_dis = requests.get('https://covid19bangladesh.pythonanywhere.com/dhaka').json()
    except:
        return ["server is bad", 0]
    fails = 0
    success = 0
    for dis in all_dis:
        try:
            CoronaInfoA.objects.get_or_create(name=dis['name'])
            dis_obj = CoronaInfoA.objects.get(name=dis['name'])
            dis_obj.bnName = dis['bnName']
            dis_obj.cases = dis['confirmed']
            dis_obj.save()
            success += 1
        except:
            fails += 1
    return [fails, success]


def c_update():
    try:
        all_c = requests.get('https://disease.sh/v2/countries?yesterday=false&allowNull=false').json()
    except:
        return ["Server is bad", 0]
    fails = 0
    success = 0
    for cnt in all_c:
        try:
            CoronaInfoC.objects.get_or_create(country=cnt['country'])
            cnt_obj = CoronaInfoC.objects.get(country=cnt['country'])
            cnt_obj.updated = cnt['updated']
            cnt_obj.cases = cnt['cases']
            if cnt['todayCases']:
                cnt_obj.todayCases = cnt['todayCases']
            cnt_obj.deaths = cnt['deaths']
            if cnt['todayDeaths']:
                cnt_obj.todayDeaths = cnt['todayDeaths']
            cnt_obj.recovered = cnt['recovered']
            if cnt['todayRecovered']:
                cnt_obj.todayRecovered = cnt['todayRecovered']
            cnt_obj.active = cnt['active']
            cnt_obj.critical = cnt['critical']
            cnt_obj.casesPerOneMillion = cnt['casesPerOneMillion']
            cnt_obj.deathsPerOneMillion = cnt['deathsPerOneMillion']
            cnt_obj.tests = cnt['tests']
            cnt_obj.testsPerOneMillion = cnt['testsPerOneMillion']
            cnt_obj.recoveredPerOneMillion = cnt['recoveredPerOneMillion']
            cnt_obj.save()
            success += 1
        except:
            fails += 1
    return [fails, success]


def country_translator(name):
    data = {
        'Bangladesh': 'বাংলাদেশ',
        'USA': 'যুক্তরাষ্ট্র',
        'Italy': 'ইতালি',
        'Spain': 'স্পেন',
        'Germany': 'জার্মানি',
        'France': 'ফ্রান্স',
        'Iran': 'ইরান',
        'UK': 'যুক্তরাজ্য',
        'China': 'চীন',
        'Switzerland': 'সুইজারল্যান্ড',
        'Belgium': 'বেলজিয়াম',
        'Turkey': 'তুরস্ক',
        'Netherlands': 'নেদারল্যান্ডস',
        'Austria': 'অস্ট্রিয়া',
        'S. Korea': 'এস কোরিয়া',
        'Canada': 'কানাডা',
        'Portugal': 'পর্তুগাল',
        'Brazil': 'ব্রাজিল',
        'Israel': 'ইস্রায়েলের',
        'Australia': 'অস্ট্রেলিয়া',
        'Norway': 'নরওয়ে',
        'Sweden': 'সুইডেন',
        'Czechia': 'Czechia',
        'Ireland': 'আয়ারল্যান্ড',
        'Malaysia': 'মালয়েশিয়া',
        'Denmark': 'ডেনমার্ক',
        'Russia': 'রাশিয়া',
        'Chile': 'চিলি',
        'Poland': 'পোল্যান্ড',
        'Philippines': 'ফিলিপাইন',
        'Ecuador': 'ইকুয়েডর',
        'Romania': 'রুমানিয়া',
        'Japan': 'জাপান',
        'Luxembourg': 'লাক্সেমবার্গ',
        'Pakistan': 'পাকিস্তান',
        'Thailand': 'থাই',
        'Indonesia': 'ইন্দোনেশিয়া',
        'India': 'ভারত',
        'Saudi Arabia': 'সৌদি আরব',
        'Finland': 'ফিন্ল্যাণ্ড',
        'South Africa': 'দক্ষিন আফ্রিকা',
        'Greece': 'গ্রীস',
        'Mexico': 'মেক্সিকো',
        'Panama': 'পানামা',
        'Iceland': 'আইসলণ্ড',
        'Dominican Republic': 'ডোমিনিকান প্রজাতন্ত্র',
        'Peru': 'পেরু',
        'Argentina': 'আর্জেন্টিনা',
        'Singapore': 'সিঙ্গাপুর',
        'Colombia': 'কলোমবিয়া',
        'Serbia': 'সার্বিয়া',
        'Croatia': 'ক্রোয়েশিয়া',
        'Slovenia': 'স্লোভেনিয়া',
        'Qatar': 'কাতার',
        'Estonia': 'এস্তোনিয়া',
        'Hong Kong': 'হংকং',
        'Algeria': 'আলজেরিয়া',
        'Egypt': 'মিশর',
        'New Zealand': 'নিউজিল্যান্ড',
        'Iraq': 'ইরাক',
        'Ukraine': 'ইউক্রেন',
        'UAE': 'সংযুক্ত আরব আমিরাতের',
        'Morocco': 'মরক্কো',
        'Lithuania': 'লিত্ভা',
        'Armenia': 'আর্মেনিয়া',
        'Bahrain': 'বাহরাইন',
        'Hungary': 'হাঙ্গেরি',
        'Lebanon': 'লেবাননের',
        'Bosnia and Herzegovina': 'বসনিয়া ও হার্জেগোভিনা',
        'Latvia': 'লাত্ভিয়া',
        'Bulgaria': 'বুলগেরিয়া',
        'Slovakia': 'শ্লোভাকিয়া',
        'Tunisia': 'টিউনিস্',
        'Andorra': 'এ্যান্ডোরা',
        'Kazakhstan': 'কাজাকস্থান',
        'Moldova': 'মোল্দাভিয়া',
        'Costa Rica': 'কোস্টারিকা',
        'Uruguay': 'উরুগুয়ে',
        'North Macedonia': 'উত্তর ম্যাসেডোনিয়া',
        'Taiwan': 'তাইওয়ান',
        'Kuwait': 'কুয়েত',
        'Azerbaijan': 'আজারবাইজান',
        'Jordan': 'জর্ডান',
        'Cyprus': 'সাইপ্রাস',
        'Burkina Faso': 'বুর্কিনা ফাসো',
        'Réunion': 'রিইউনিয়ন',
        'Albania': 'আলবেনিয়া',
        'San Marino': 'সান মারিনো',
        'Cameroon': 'ক্যামেরুন',
        'Vietnam': 'ভিয়েতনাম',
        'Oman': 'ওমান',
        'Afghanistan': 'আফগানিস্তান',
        'Ghana': 'ঘানা',
        'Cuba': 'কিউবা',
        'Ivory Coast': 'আইভরি কোস্ট',
        'Senegal': 'সেনেগাল',
        'Uzbekistan': 'উজ্বেকিস্থান',
        'Faeroe Islands': 'ফেরো দ্বীপপুঞ্জ',
        'Honduras': 'হন্ডুরাস',
        'Malta': 'মাল্টা',
        'Belarus': 'বেলারুশ',
        'Channel Islands': 'চ্যানেল দ্বীপপুঞ্জ',
        'Mauritius': 'মরিশাস',
        'Venezuela': 'ভেনেজুয়েলা',
        'Sri Lanka': 'শ্রীলংকা',
        'Nigeria': 'নাইজেরিয়া',
        'Palestine': 'প্যালেস্টাইন',
        'Brunei': 'ব্রুনেই',
        'Martinique': 'মার্টিনিক',
        'Montenegro': 'মন্টিনিগ্রো',
        'Bolivia': 'বলিভিয়া',
        'Georgia': 'জর্জিয়া',
        'Guadeloupe': 'গুয়াডেলোপ',
        'Kyrgyzstan': 'কিরগিজস্তান',
        'DRC': 'ডি আর সি',
        'Cambodia': 'কাম্বোজ',
        'Mayotte': 'মায়োত্তে',
        'Trinidad and Tobago': 'ত্রিনিদাদ ও টোবাগো',
        'Rwanda': 'রুয়ান্ডা',
        'Paraguay': 'প্যারাগুয়ে',
        'Gibraltar': 'জিব্রাল্টার',
        'Liechtenstein': 'লিচেনস্টেইন',
        'Isle of Man': 'আইল অফ ম্যান',
        'Kenya': 'কেনিয়া',
        'Madagascar': 'মাদাগাস্কার',
        'Aruba': 'আরুবা',
        'Monaco': 'মোনাকো',
        'French Guiana': 'একটি দেশের নাম',
        'Uganda': 'উগান্ডা',
        'Macao': 'ম্যাকাও',
        'Guatemala': 'গুয়াতেমালা',
        'Jamaica': 'জামাইকা',
        'French Polynesia': 'ফরাসি পলিনেশিয়া',
        'Zambia': 'জাম্বিয়া',
        'Niger': 'নাইজার',
        'Togo': 'যাও',
        'Barbados': 'বার্বাডোস',
        'El Salvador': 'এল সালভাদর',
        'Bermuda': 'বারমুডা',
        'Djibouti': 'জিবুতি',
        'Ethiopia': 'ইথিওপিয়া',
        'Mali': 'মালি',
        'Guinea': 'গিনি',
        'Tanzania': 'তাঞ্জানিয়া',
        'Congo': 'কঙ্গো',
        'Gabon': 'গ্যাবন',
        'Maldives': 'মালদ্বীপ',
        'Saint Martin': 'সেন্ট মার্টিন',
        'Haiti': 'হাইতি',
        'New Caledonia': 'নতুন ক্যালেডোনিয়া',
        'Myanmar': 'মায়ানমার',
        'Equatorial Guinea': 'নিরক্ষীয় গিনি',
        'Eritrea': 'ইরিত্রিয়া',
        'Cayman Islands': 'কেম্যান দ্বীপপুঞ্জ',
        'Mongolia': 'মঙ্গোলিয়া',
        'Saint Lucia': 'সেন্ট লুসিয়া',
        'Guyana': 'গায়ানা',
        'Dominica': 'ডোমিনিকা',
        'Curaçao': 'কিউরাসাও',
        'Namibia': 'নামিবিয়া',
        'Syria': 'সিরিয়া',
        'Greenland': 'গ্রীনল্যান্ড',
        'Laos': 'লাওস',
        'Libya': 'লিবিয়া',
        'Seychelles': 'সিসিলি',
        'Suriname': 'সুরিনাম',
        'Benin': 'বেনিন',
        'Grenada': 'গ্রেনাডা',
        'Eswatini': 'Eswatini',
        'Zimbabwe': 'জিম্বাবুয়ে',
        'Guinea-Bissau': 'গিনি-বিসাউ',
        'Mozambique': 'মোজাম্বিক',
        'Saint Kitts and Nevis': 'সেন্ট কিটস ও নেভিস',
        'Angola': 'অ্যাঙ্গোলা',
        'Sudan': 'সুদান',
        'Antigua and Barbuda': 'অ্যান্টিগুয়া ও বার্বুডা',
        'Chad': 'চাদ',
        'Cabo Verde': 'ক্যাবো ভার্দে',
        'Mauritania': 'মরিতানিয়া',
        'Vatican City': 'ভ্যাটিকান সিটি',
        'Liberia': 'লাইবেরিয়া',
        'St. Barth': 'সেন্ট বার্থ',
        'Sint Maarten': 'সিন্ট মার্টেন',
        'Nicaragua': 'নিকারাগুয়া',
        'Nepal': 'নেপাল',
        'Fiji': 'ফিজি',
        'Montserrat': 'মন্টসেরাট',
        'Somalia': 'সোমালিয়া',
        'Turks and Caicos': 'টার্কস এবং কাইকোস',
        'Botswana': 'বতসোয়ানা',
        'Gambia': 'গাম্বিয়া',
        'Bhutan': 'ভুটান',
        'Belize': 'বেলিজ',
        'British Virgin Islands': 'ব্রিটিশ ভার্জিন দ্বীপপুঞ্জ',
        'CAR': 'গাড়িতে',
        'Anguilla': 'এ্যাঙ্গুইলা',
        'Burundi': 'বুরুন্ডি',
        'Papua New Guinea': 'পাপুয়া নিউ গিনি',
        'St. Vincent Grenadines': 'সেন্ট ভিনসেন্ট গ্রেনাডাইনস',
        'Sierra Leone': 'সিয়েরা লিওন',
        'Timor-Leste': 'পূর্ব তিমুর',
    }
    try:
        return data[name]
    except:
        return name


def digit_translator(number):
    data3 = str(number)
    data4 = ''
    for m in data3:
        if m == '1':
            data4 += '১'
        elif m == '2':
            data4 += '২'
        elif m == '3':
            data4 += '৩'
        elif m == '4':
            data4 += '৪'
        elif m == '5':
            data4 += '৫'
        elif m == '6':
            data4 += '৬'
        elif m == '7':
            data4 += '৭'
        elif m == '8':
            data4 += '৮'
        elif m == '9':
            data4 += '৯'
        elif m == '0':
            data4 += '০'
        else:
            data4 += m
    return data4


def update(name):
    UpdateTime.objects.get_or_create(topic='corona_api' + name)
    pre = UpdateTime.objects.get(topic='corona_api' + name)
    now = int(datetime.now().strftime("%H")) * 60 + int(datetime.now().strftime("%m"))
    if abs(int(pre.time) - now) >= 60:
        if name == 'c':
            c_update()
        if name == 'd':
            d_update()
        if name == 'a':
            a_update()
        pre.time = now
        pre.save()
