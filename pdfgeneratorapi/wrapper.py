# -*- coding: utf-8 -*-

"""
pdfgeneratorapi.wrapper
~~~~~~~~~~~~~~~

This module contains the resource wrapper for PDFGeneratorAPI.com.
"""

import hashlib
import hmac
import json
import os
import sys
import urllib

import requests
from .constants import ALL_DOCUMENT_FORMATS, ALL_RESPONSE_FORMATS, ALL_ACCESS_TYPES
from .decorators import make_response
from .exceptions import IncorrectParameterError, RequiredParameterMissing


class APIBase(object):
    """ The base class for the PDFGeneratorAPI.com Wrapper.

    :param api_key: API Key for PDFGeneratorAPI.com(found under your Account Settings).
                    Preferred: Load from environment.
    :param api_secret: API Secret Key for PDFGeneratorAPI.com(found under your Account Settings).
                       Preferred: Load from environment.
    :param workspace: Name of your workspace. The email you signed up with on PDFGeneratorAPI.com.
                      Preferred: Load from environment.
    :param document_format: Document format. Available formats: (pdf, html, zip) Default: pdf.
    :param response_format: Response format. Available formats: (base64, url, I). Default: base64.
    :param signature_auth: Response format. Available formats: (base64, url, I). Default: False.
    :param region: The region of the server. Basically the subdomain.
                   This wrapper was made considering `us1` subdomain.
    :param version: The version of the PDFGeneratorAPI.com. This wrapper was made in consideration of v3.
    :param api_url: The complete base url of the PDFGeneratorAPI excluding the resource endpoints.
    """

    def __init__(self, **kwargs):
        self.__api_key = kwargs.get("api_key", os.environ.get("PDF_GENERATOR_KEY"))
        self.__api_secret = kwargs.get(
            "api_secret", os.environ.get("PDF_GENERATOR_SECRET")
        )
        self.__workspace = kwargs.get(
            "workspace", os.environ.get("PDF_GENERATOR_WORKSPACE")
        )
        if not (self.__api_key and self.__api_secret and self.__workspace):
            raise RequiredParameterMissing("Missing API Required Parameters")
        self.document_format = kwargs.get("document_format", "pdf")
        self.response_format = kwargs.get("response_format", "base64")
        self.signature_auth = kwargs.get("signature_auth", True)

        self.region = kwargs.get("region", "us1")
        self.version = kwargs.get("version", "v3")

        api_url = (
            "https://" + self.region + ".pdfgeneratorapi.com/api/" + self.version + "/"
        )
        self.API_URL = kwargs.get("api_url", api_url)

        self._validate_formats(self.document_format, self.response_format)

    def _validate_formats(self, document_format, response_format):
        if response_format not in ALL_RESPONSE_FORMATS:
            raise IncorrectParameterError(
                "{0} is an invalid output format.".format(self.response_format)
            )
        if document_format not in ALL_DOCUMENT_FORMATS:
            raise IncorrectParameterError(
                "{0} is an invalid document format.".format(self.document_format)
            )

    def _get_signature(self, resource):
        """ Generates a signature based on `api_key`, `workspace` and `api_secret`. """
        message = self.__api_key + resource + self.__workspace
        signature = hmac.new(
            bytes(self.__api_secret, "UTF-8"), bytes(message, "UTF-8"), hashlib.sha256
        ).hexdigest()
        return signature

    def prepare_auth_params(self, resource):
        """ Prepares auth params for one-click URL generation. Used in editor URL.
        :param resource: Resource endpoint that needs to be hit. ..API_URL../<RESOURCE>
        Returns a <dict>.
        """
        # Always use signature auth here. Simple Auth would expose secret key.
        query_params = {
            "key": self.__api_key,
            "signature": self._get_signature(resource),
            "workspace": self.__workspace,
        }
        return query_params

    def prepare_headers(self, resource: str = None):
        """ Prepares headers for API request. Supports both Simple and Signature Auth.
        :param resource: Resource endpoint that needs to be hit. ..API_URL../<RESOURCE>
        Returns a <dict>.
        """
        import pdfgeneratorapi

        user_agent = "pdfgeneratorapi/{api_region}/{api_version} Python/{package_version}/{sys_version}".format(
            package_version=pdfgeneratorapi.__version__,
            sys_version=sys.version.split(" ", 1)[0],
            api_region=self.region,
            api_version=self.version,
        )
        if self.signature_auth is True:
            if not resource:
                raise Exception(
                    "Signature Auth requires resource for signature creation."
                )
            header_auth = {"X-Auth-Signature": self._get_signature(resource)}
        else:
            header_auth = {"X-Auth-Secret": self.__api_secret}
        request_headers = {
            "X-Auth-Key": self.__api_key,
            "X-Auth-Workspace": self.__workspace,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": user_agent,
        }
        request_headers.update(header_auth)
        return request_headers


class PDFGenerator(APIBase):
    """ The actual resource class which communicates with the API.
    Functions under this class:
        all_templates()
        get_template()
        create_template()
        create_template_copy()
        delete_template()
        create_document()
        get_editor_url()

    Usage::

      >>> from pdfgeneratorapi import PDFGenerator
      >>> pdfg_client = PDFGenerator()
    """

    @make_response
    def all_templates(self, access: list = None, tags: list = None):
        """ Returns list of templates in the workspace.
        
        :param access: Allows to filter templates by access type.
                       Comma separated list of access types. [`organization`, `private`]
        :param tags: Allows to filter templates by assigned tags.
                     Comma separated list of tags assigned to template.

        Usage::

          >>> pdfg_client.all_template()
           [List of <PDFGeneratorResponse>]
        """
        resource = "templates"
        request_params = {}
        if access:
            if any(access) in ALL_ACCESS_TYPES:
                request_params.update({"access": access})
            else:
                raise Exception
        if tags:
            if type(tags) is list:
                request_params.update({"tags": tags})
            else:
                raise Exception
        response = requests.get(
            url=self.API_URL + resource,
            headers=self.prepare_headers(resource),
            params=request_params,
        )
        return response

    @make_response
    def get_template(self, template_id: int):
        """ Returns template configuration.

        :param template_id: Unique ID of the template.

        Usage::

          >>> pdfg_client.get_template(template_id=123)
           <PDFGeneratorResponse>
        """
        resource = "templates/{0}".format(str(template_id))
        response = requests.get(
            url="{base_url}{resource}".format(base_url=self.API_URL, resource=resource),
            headers=self.prepare_headers(resource),
        )
        # TODO: Great to have: ...get_template(template_id=123).delete()
        # TODO: Great to have: ...get_template(template_id=123).copy(name='first_copy')
        return response

    @make_response
    def create_template(self, name):
        """ Creates a blank template with given name. 
        
        :param name: Name of the newly created template.

        Usage::

          >>> pdfg_client.create_template(name='one_template')
           <PDFGeneratorResponse>
        """
        resource = "templates"
        response = requests.post(
            url=self.API_URL + resource,
            headers=self.prepare_headers(resource),
            json={"name": name},
        )
        return response

    @make_response
    def create_template_copy(self, template_id: int, name: str):
        """ Creates a copy of a template to the workspace.

        :param template_id: Unique ID of the template.
        :param name: Name of the newly created template.

        Usage::

          >>> pdfg_client.create_template_copy(template_id=123, name='one_template')
           <PDFGeneratorResponse>
        """
        resource = "templates/{template_id}/copy".format(template_id=str(template_id))
        request_params = {"name": name}
        response = requests.post(
            url=self.API_URL + resource,
            headers=self.prepare_headers(resource),
            params=request_params,
        )
        return response

    @make_response
    def delete_template(self, template_id: int):
        """ Deletes a Template.

        :param template_id: Unique ID of the template.

        Usage::

          >>> pdfg_client.delete_template(template_id=123)
           <bool>
        """
        resource = "templates/{template_id}".format(template_id=str(template_id))
        response = requests.delete(
            url=self.API_URL + resource, headers=self.prepare_headers(resource)
        )
        return response

    @make_response
    def create_document(
        self,
        template_id: int,
        data: dict,
        document_format: str = None,
        response_format: str = None,
    ):
        """ Merges template with data and returns base64 encoded document or public url to a document.
            In simple words, Create/Generate a Document.

        :param template_id: Unique ID of the template.
        :param data: A dict of data that is needed to fill the PDF.
        :param document_format: Document format. Available formats: (pdf, html, zip) Default: pdf.
        :param response_format: Response format. Available formats: (base64, url, I). Default: base64.

        Usage::

          >>> pdfg_client.create_document(template_id=123, data={'name': 'Sameer Kumar'})
           <PDFGeneratorResponse>
        """
        document_format = (
            self.document_format if document_format is None else document_format
        )
        response_format = (
            self.response_format if response_format is None else response_format
        )
        self._validate_formats(document_format, response_format)
        resource = "templates/{template_id}/output".format(template_id=str(template_id))
        request_params = {"format": document_format, "output": response_format}
        response = requests.post(
            url=self.API_URL + resource,
            headers=self.prepare_headers(resource),
            params=request_params,
            json=data,
        )
        return response

    def get_editor_url(self, template_id: int, data):
        """ Prepares and returns a one-click URL to the web editor.

        :param template_id: Unique ID of the template.
        :param data: data to be pre-filled in the web editor.

        Usage::

          >>> pdfg_client.get_editor_url(template_id=123, data={'name': 'Sameer Kumar'})
           <str>
        """
        if not type(data) is str:
            data = json.dumps(data)

        resource = "templates/{template_id}/editor".format(template_id=str(template_id))
        request_params = self.prepare_auth_params(resource=resource)
        request_params.update({"data": data})
        url = "{base_url}{resource}?{query_string}".format(
            base_url=self.API_URL,
            resource=resource,
            query_string=urllib.parse.urlencode(request_params),
        )
        return url
