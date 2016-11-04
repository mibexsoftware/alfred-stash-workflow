# -*- coding: utf-8 -*-

from unittest import TestCase
from datetime import datetime

from src.util import pretty_timestamp


class UtilTest(TestCase):

    def test_pretty_timestamp(self):
        self.assertEquals('19 hours ago', pretty_timestamp(1478187004, now=datetime(2016, 11, 04, 12, 00, 00)))
        self.assertEquals('Yesterday', pretty_timestamp(1478187004, now=datetime(2016, 11, 05, 12, 00, 00)))
        self.assertEquals('2 days ago', pretty_timestamp(1478187004, now=datetime(2016, 11, 06, 12, 00, 00)))
        self.assertEquals('1 week(s) ago', pretty_timestamp(1478187004, now=datetime(2016, 11, 11, 12, 00, 00)))
        self.assertEquals('1 month(s) ago', pretty_timestamp(1478187004, now=datetime(2016, 12, 11, 12, 00, 00)))
        self.assertEquals('1 year(s) ago', pretty_timestamp(1478187004, now=datetime(2017, 11, 11, 12, 00, 00)))
