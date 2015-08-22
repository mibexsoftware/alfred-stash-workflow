#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from src.routing import route
from src.util import workflow


def main(wf):
    route(wf.args)


if __name__ == '__main__':
    sys.exit(workflow().run(main))
