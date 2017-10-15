#! /usr/bin/env python3

import logging
import os.path
import sys

import pathvalidate
import regex

import REDsym.actions


if sys.argv[1] == "update":
    REDsym.actions.update_wm2(inplace=True)
