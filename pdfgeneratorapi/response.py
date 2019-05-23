# -*- coding: utf-8 -*-

"""
pdfgeneratorapi.response
~~~~~~~~~~~~~~~

This module contains the response class.
"""

from dateutil.parser import parse
import re


def convert_snake_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class PDFGeneratorResponse(object):
    # Source - https://stackoverflow.com/a/6993694/7448094
    def __init__(self, data):
        for name, value in data.items():
            try:
                # string to datetime
                value = parse(value)
            except (ValueError, TypeError):
                pass
            setattr(self, convert_snake_case(name), self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return PDFGeneratorResponse(value) if isinstance(value, dict) else value
