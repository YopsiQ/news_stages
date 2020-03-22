# -*- coding: utf-8 -*-
import json
import os
import re
import urllib
from datetime import datetime

from hstest.django_test import DjangoTest
from hstest.check_result import CheckResult


class HyperNewsTest(DjangoTest):
    COMMON_LINK_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>'''
    H2_PATTERN = r'<h2>(?P<h2>.*)</h2>'
    H4_PATTERN = r'<h4>(?P<h4>.*)</h4>'
    PARAGRAPH_PATTERN = r'<p>(?P<p>.*)</p>'
    FIRST_GROUPS_PATTERN = '<h4>.*?</h4>.*?<ul>.+?</ul>'
    SECOND_GROUPS_PATTERN = (
        '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>(.+?)</a>'''
    )

    def __init__(self, *args, **kwargs):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.news_file_name = 'news.json'
        os.environ['NEWS_JSON_PATH'] = os.path.join(current_dir,
                                                    self.news_file_name)
        super().__init__(*args, **kwargs)

    def __setup(self):
        self.news_data = [{
            'created': '2020-02-09 14:15:10',
            'text': 'Text of the news 1',
            'title': 'News 1',
            'link': '1'
        }, {
            'created': '2020-02-10 14:15:10',
            'text': 'Text of the news 2',
            'title': 'News 2',
            'link': '2'
        }, {
            'created': '2020-02-09 16:15:10',
            'text': 'Text of the news 3',
            'title': 'News 3',
            'link': '3'
        }]
        with open(self.news_file_name, 'w') as f:
            json.dump(self.news_data, f)

    def check_main_header(self) -> CheckResult:
        self.__setup()
        try:
            page = self.read_page(f'http://localhost:{self.port}/news')
        except urllib.error.URLError:
            return CheckResult.false(
                'Cannot connect to the main page.'
            )

        h2_headers = re.findall(self.H2_PATTERN, page)
        main_header = 'Hyper news'

        if main_header not in h2_headers:
            return CheckResult.false(
                'Main page should contain <h2> element with text "Hyper news"'
            )

        return CheckResult.true()

    def check_news_page(self) -> CheckResult:
        self.__setup()
        testing_news = self.news_data[0]
        link = testing_news['link']
        created = testing_news['created']

        created_dt = datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
        created_date_str = created_dt.strftime('%Y-%m-%d')

        try:
            page = self.read_page(f'http://localhost:{self.port}/news/{link}')
        except urllib.error.URLError:
            return CheckResult.false(
                'Cannot connect to the news page.'
            )

        page_headers = re.findall(self.H2_PATTERN, page)
        page_paragraphs = re.findall(self.PARAGRAPH_PATTERN, page)
        if testing_news['title'] not in page_headers:
            return CheckResult.false(
                'News page should contain <h2> element with the data '
                'of the title field from json file'
            )

        if testing_news['text'] not in page_paragraphs:
            return CheckResult.false(
                'News page should contain <p> element with the data '
                'of the text field from json file'
            )

        if created_date_str not in page_paragraphs:
            return CheckResult.false(
                'News page should contain <p> element with the data '
                'of the created field from json file '
                'in the format: "2099-09-09"'
            )

        return CheckResult.true()

    def check_news_page_main_link(self):
        self.__setup()
        main_link = '/news/'

        testing_news = self.news_data[0]
        link = testing_news['link']

        try:
            page = self.read_page(f'http://localhost:{self.port}/news/{link}')
        except urllib.error.URLError:
            return CheckResult.false(
                'Cannot connect to the news page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page)

        if main_link not in links_from_page:
            return CheckResult.false(
                f'News page should contain <a> element with href {main_link}'
            )

        return CheckResult.true()

    def check_main_page(self) -> CheckResult:
        self.__setup()
        created_set = set()
        for news in self.news_data:
            created_dt = datetime.strptime(news['created'],
                                           '%Y-%m-%d %H:%M:%S') \
                                 .date()
            created_set.add(created_dt)

        created_list = [x for x in created_set]
        created_list.sort(reverse=True)
        created_list_str = [x.strftime('%Y-%m-%d') for x in created_list]

        try:
            page = self.read_page(f'http://localhost:{self.port}/news')
        except urllib.error.URLError:
            return CheckResult.false(
                'Cannot connect to the main page.'
            )

        h4_headers = re.findall(self.H4_PATTERN, page)
        filtered_h4 = list(filter(lambda x: x in created_list_str, h4_headers))

        if filtered_h4 != created_list_str:
            return CheckResult.false(
                'Main page should contain <h4> elements grouped by '
                'date created and first should be fresh news.'
            )

        for news in self.news_data:
            created_date = datetime.strptime(news['created'],
                                             '%Y-%m-%d %H:%M:%S') \
                .date()
            news['created_date'] = created_date
            news['created_date_str'] = created_date.strftime('%Y-%m-%d')
            news['link'] = '/news/{}/'.format(news['link'])

        file_data = sorted(self.news_data, key=lambda x: x['title'])
        file_data = sorted(
            file_data, key=lambda x: x['created_date'], reverse=True)

        for news in file_data:
            news.pop('created_date')
            news.pop('created')
            news.pop('text')

        groups = re.findall(self.FIRST_GROUPS_PATTERN, page, re.S)
        news_list = [
            sorted(re.findall(self.SECOND_GROUPS_PATTERN, group, re.S),
                   key=lambda news: news[1])
            for group in groups
        ]
        response_data = []
        for news_l, h4 in zip(news_list, filtered_h4):
            for news in news_l:
                response_data.append({
                    'created_date_str': h4,
                    'link': news[0],
                    'title': news[1]
                })

        if response_data != file_data:
            return CheckResult.false(
                'Main page should contain <a> elements with href to news pages.'
            )


        return CheckResult.true()
