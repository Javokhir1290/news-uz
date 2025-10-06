from common.models import *
import requests as rq


def valyuta():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = rq.get(url).json()
    return response




def main(request):
    ctgs = Category.objects.filter(is_menu=True)
    svejiy_news = New.objects.all().order_by('-id')

    return {
        'valyuta': valyuta(),
        'ctgs': ctgs,
        'svejiy_news': svejiy_news,
    }