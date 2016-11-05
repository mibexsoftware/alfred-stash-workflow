# -*- coding: utf-8 -*-

from unittest import TestCase
from datetime import datetime

import pytz as pytz
from src.util import pretty_date


class UtilTest(TestCase):

    def test_pretty_timestamp(self):
        my_time = pytz.utc.localize(datetime.utcfromtimestamp(1478187004))  # Thu, 03 Nov 2016 15:30:04 GMT
        self.assertEquals('20 hours ago', pretty_date(my_time, now=datetime(2016, 11, 04, 12, 0, 0, 0, pytz.UTC)))
        self.assertEquals('Yesterday', pretty_date(my_time, now=datetime(2016, 11, 05, 12, 0, 0, 0, pytz.UTC)))
        self.assertEquals('2 days ago', pretty_date(my_time, now=datetime(2016, 11, 06, 12, 0, 0, 0, pytz.UTC)))
        self.assertEquals('1 week(s) ago', pretty_date(my_time, now=datetime(2016, 11, 11, 12, 0, 0, 0, pytz.UTC)))
        self.assertEquals('1 month(s) ago', pretty_date(my_time, now=datetime(2016, 12, 11, 12, 0, 0, 0, pytz.UTC)))
        self.assertEquals('1 year(s) ago', pretty_date(my_time, now=datetime(2017, 11, 11, 12, 0, 0, 0, pytz.UTC)))
