import itertools
import json
from datetime import datetime
from json.decoder import JSONDecodeError

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader


def adding_page(request):
    template = loader.get_template('news/adding_page.html')

    return HttpResponse(template.render({}, request))


def create(request):
    with open(settings.NEWS_JSON_PATH, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    links = [int(x['link']) for x in news_data]
    new_link = str(max(links)+1) if links else '1'

    fresh_news = {
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'link': new_link,
        'title': request.POST.get('title'),
        'text': request.POST.get('text'),
    }
    news_data.append(fresh_news)

    with open(settings.NEWS_JSON_PATH, 'w') as file_object:
        json.dump(news_data, file_object)

    return redirect('index')


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

    template = loader.get_template('news/detail.html')
    context = {
       'item': news_item
    }
    return HttpResponse(template.render(context, request))


def search(request):
    search_string = request.GET.get('search_string')

    with open(settings.NEWS_JSON_PATH, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    template = loader.get_template('news/index.html')
    news_data = [x for x in news_data if search_string in x['title']]

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
        'search_string': search_string,
    }
    return HttpResponse(template.render(context, request))
