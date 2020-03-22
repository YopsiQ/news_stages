# -*- coding: utf-8 -*-
import json
import os
import re
import urllib

from hstest.django_test import DjangoTest
from hstest.check_result import CheckResult


class HyperNewsTest(DjangoTest):
    H2_PATTERN = '<h2>(.*)</h2>'

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
            page = self.read_page(f'http://localhost:{self.port}/news/')
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
