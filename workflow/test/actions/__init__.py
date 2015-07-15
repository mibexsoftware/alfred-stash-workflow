# -*- coding: utf-8 -*-


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other
