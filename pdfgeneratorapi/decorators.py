# -*- coding: utf-8 -*-

"""
pdfgeneratorapi.decorators
~~~~~~~~~~~~~~~

This module contains decorator used in the wrapper.
"""

from requests.exceptions import RequestException, HTTPError
from .utils import dict_to_object
from .exceptions import (
    ResourceEntityNotFound,
    PDFGeneratorAPIException,
    AuthenticationParameterError,
    IncorrectParameterError,
    InternalServerError,
    AccessNotGrantedError,
)


def make_response(func):
    def to_object(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            status_code = http_err.response.status_code
            if status_code == 401:
                raise AccessNotGrantedError(http_err, response)
            if status_code == 403:
                raise AuthenticationParameterError(http_err, response)
            if status_code == 404:
                raise ResourceEntityNotFound(http_err, response)
            if status_code == 422:
                raise AuthenticationParameterError(http_err, response)
            if status_code == 500:
                raise InternalServerError(http_err, response)
        except RequestException as req_err:
            raise PDFGeneratorAPIException(req_err, response)

        response_dict = response.json()
        return dict_to_object(response_dict)

    return to_object
