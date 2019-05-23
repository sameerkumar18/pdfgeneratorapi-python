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
from .constants import ALL_OUTPUT_FORMATS, ALL_DOCUMENT_FORMATS, ALL_ACCESS_TYPES
from .decorators import make_response


class APIBase(object):
    """ The base class for the PDFGeneratorAPI.com Wrapper.

    :param api_key: API Key for PDFGeneratorAPI.com(found under your Account Settings). Preferred: Load from environment.
    :param api_secret: API Secret Key for PDFGeneratorAPI.com(found under your Account Settings).
                       Preferred: Load from environment.
    :param workspace: Name of your workspace. The email you signed up with on PDFGeneratorAPI.com.
                      Preferred: Load from environment.
    :param document_format: Document format. Available formats: (pdf, html, zip) Default: pdf.
    :param response_format: Response format. Available formats: (base64, url, I). Default: base64.
    :param signature_auth: Response format. Available formats: (base64, url, I). Default: False.
    :param region: The region of the server. Basically the subdomain. This wrapper was made in consideration of us1.
    :param version: The version of the PDFGeneratorAPI.com. This wrapper was made in consideration of v3.
    :param complete_url: The complete base url of the PDFGeneratorAPI before the resource endpoints.
    """

    def __init__(self, **kwargs):
        self.__api_key = kwargs.get("api_key", os.environ.get(""))
        self.__api_secret = kwargs.get("api_secret", os.environ.get(""))
        self.__workspace = kwargs.get("workspace", os.environ.get(""))  # )
        self.document_format = kwargs.get("document_format", "pdf")  # Document format.
        self.response_format = kwargs.get("response_format", "base64")
        self.signature_auth = kwargs.get("signature_auth", True)

        if self.response_format not in ALL_OUTPUT_FORMATS:
            # raise e
            pass
        if self.document_format not in ALL_DOCUMENT_FORMATS:
            # raise e
            pass

        self.region = kwargs.get("region", "us1")
        self.version = kwargs.get("version", "v3")

        complete_url = (
            "https://" + self.region + ".pdfgeneratorapi.com/api/" + self.version + "/"
        )
        self.API_URL = kwargs.get("complete_url", complete_url)

    def _prepare_headers(self, resource: str = None, params: bool = False):
        """ Prepares headers for API request. Supports both Simple and Signature Auth.
        :param resource: Resource endpoint that needs to be hit. ..API.com/<RESOURCE>
        :param params: Returns the parameters which provide auth in case of one-click Editor URL generation.
        Returns a <dict>.
        """

        def _get_signature():
            """ Generates a signature based on `api_key`, `workspace` and `api_secret`. """
            message = self.__api_key + resource + self.__workspace
            signature = hmac.new(
                bytes(self.__api_secret, "UTF-8"),
                bytes(message, "UTF-8"),
                hashlib.sha256,
            ).hexdigest()
            return signature

        def _prepare_auth_params():
            """ Prepares auth params for one-click URL generation. Used in editor URL. """
            # Always use signature auth here. Simple Auth would expose secret key.
            query_params = {
                "key": self.__api_key,
                "signature": _get_signature(),
                "workspace": self.__workspace,
            }
            return query_params

        if params:
            return _prepare_auth_params()
        user_agent = "pdfgeneratorapi/%s Python/%s".format(
            package_version="",
            sys_version=sys.version.split(" ", 1)[0],
            api_region=self.region,
            api_version=self.version,
        )
        if self.signature_auth is True:
            if not resource:
                raise Exception(
                    "Signature Auth requires resource for signature creation."
                )
            header_auth = {"X-Auth-Signature": _get_signature()}
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
        
        :param access: Allows to filter templates by access type. Comma separated list of access types. [`organization`, `private`]
        :param tags: Allows to filter templates by assigned tags. Comma separated list of tags assigned to template.

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
            headers=self._prepare_headers(resource),
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
            headers=self._prepare_headers(resource),
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
            headers=self._prepare_headers(resource),
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
            headers=self._prepare_headers(resource),
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
            url=self.API_URL + resource, headers=self._prepare_headers(resource)
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
        resource = "templates/{template_id}/output".format(template_id=str(template_id))
        request_params = (
            (
                "format",
                self.document_format if document_format is None else document_format,
            ),
            (
                "output",
                self.response_format if response_format is None else response_format,
            ),
        )
        response = requests.post(
            url=self.API_URL + resource,
            headers=self._prepare_headers(resource),
            params=request_params,
            json=data,
        )
        # print(response.json())
        return response

    def get_editor_url(self, template_id: int, data: dict):
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
        request_params = self._prepare_headers(resource=resource, params=True)
        request_params.update({"data": data})
        url = "{base_url}{resource}?{query_string}".format(
            base_url=self.API_URL,
            resource=resource,
            query_string=urllib.parse.urlencode(request_params),
        )
        return url
