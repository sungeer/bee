#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

from src.scripts import client

if __name__ == '__main__':
    client()

