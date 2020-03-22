import itertools
import json
from datetime import datetime
from json.decoder import JSONDecodeError

from django.http import HttpResponse
from django.template import loader

from hypernews import settings


def index(request):
    with open(settings.NEWS_JSON_PATH, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    template = loader.get_template('news/index.html')

    for news in news_data:
        created_date = datetime.strptime(news['created'], '%Y-%m-%d %H:%M:%S') \
                               .date()
        news['created_date'] = created_date
        news['created_date_str'] = created_date.strftime('%Y-%m-%d')

    news_data.sort(key=lambda x: x['created_date'], reverse=True)
    an_iterator = itertools.groupby(news_data, lambda x: x['created_date_str'])

    result_news_data = [{'header': key, 'data': list(group)}
                        for key, group in an_iterator]
    context = {
        'news': result_news_data,
    }
    return HttpResponse(template.render(context, request))


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
