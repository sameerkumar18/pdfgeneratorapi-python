# -*- coding: utf-8 -*-

"""
pdfgeneratorapi.exceptions
~~~~~~~~~~~~~~~

This module contains all the custom defined exceptions.
"""

"""
https://docs.pdfgeneratorapi.com/#errors

HTTP Exception Status Codes and their description
All additional information about the error is sent in response body.


Code            Description
==========================================
401	            Authentication failed
401	            Required parameter missing
403	            Access not granted
404	            Entity not found
404	            Resource not found
422	            Incorrect parameter value
500	            Internal error

"""


class PDFGeneratorAPIException(Exception):
    def __init__(self, message=None, response=None):
        super(PDFGeneratorAPIException, self).__init__(message)
        if response:
            http_body = response.text
            http_status = response.status_code
            json_body = response.json()
            self.http_body = http_body
            self.http_status = http_status
            self.json_body = json_body


class ResourceEntityNotFound(PDFGeneratorAPIException):
    pass


class InternalServerError(PDFGeneratorAPIException):
    pass


class AccessNotGrantedError(PDFGeneratorAPIException):
    pass


class AuthenticationParameterError(PDFGeneratorAPIException):
    pass


class UnAuthorizedAccessError(PDFGeneratorAPIException):
    pass


class IncorrectParameterError(PDFGeneratorAPIException):
    pass


class RequiredParameterMissing(PDFGeneratorAPIException):
    pass


class InvalidOutputFormat(PDFGeneratorAPIException):
    pass


class InvalidFormat(PDFGeneratorAPIException):
    pass
