import json
from datetime import datetime

from django.http import HttpResponse
from django.template import loader

from hypernews import settings


def index(request):
    return HttpResponse('<h2>Hyper news</h2>')


def detail(request, news_link):
    with open(settings.NEWS_JSON_PATH, 'r') as file_object:
        news_data = json.load(file_object)

    news_item = [x for x in news_data if x['link'] == news_link][0]

    created_dt = datetime.strptime(news_item['created'], '%Y-%m-%d %H:%M:%S')
    news_item['created'] = created_dt.strftime('%Y-%m-%d')

    template = loader.get_template('news/detail.html')
    context = {
       'item': news_item
    }
    return HttpResponse(template.render(context, request))
