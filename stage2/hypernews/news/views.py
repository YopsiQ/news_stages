import json

from django.conf import settings
from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse('<h2>Hyper news</h2>')


def detail(request, news_link):
    with open(settings.NEWS_JSON_PATH, 'r') as file_object:
        news_data = json.load(file_object)

    news_item = [x for x in news_data if x['link'] == news_link][0]

    template = loader.get_template('news/detail.html')
    context = {
       'item': news_item
    }
    return HttpResponse(template.render(context, request))
