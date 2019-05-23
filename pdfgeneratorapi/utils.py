# -*- coding: utf-8 -*-

"""
pdfgeneratorapi.utils
~~~~~~~~~~~~~~~

This module contains the utility functions.
"""

import json

from .response import PDFGeneratorResponse


def create_py_object(item: dict):
    map_item = PDFGeneratorResponse(item)
    map_item.__setattr__("to_dict", item)
    map_item.__setattr__("to_json", json.dumps(item))
    return map_item


def dict_to_object(data: dict):
    response_dict = {}
    for key, value in data.items():
        if not value:
            continue
        if type(value) is dict:
            response_dict.update(value)
        if type(value) in (str, int, bool):
            response_dict.update({key: value})
        elif type(value) is list:
            response_list = []
            for element in value:
                map_item = create_py_object(element)
                response_list.append(map_item)
            return response_list
    response_object = create_py_object(response_dict)
    return response_object
