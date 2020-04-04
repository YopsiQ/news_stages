# -*- coding: utf-8 -*-
from hstest.test_case import TestCase

from base import HyperNewsTest


class HyperNewsTestRunner(HyperNewsTest):
    def generate(self):
        return [
            # 1 task
            TestCase(attach=self.check_server),
            TestCase(attach=self.check_coming_soon_page),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HyperNewsTestRunner('hypernews.manage').run_tests()
