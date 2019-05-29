[logo]: https://pdfgeneratorapi.com/assets/deploy/web/images/logo-light.png "PDFGeneratorAPI.com Python Wrapper Logo"

![alt text][logo] PDFGeneratorAPI.com Python wrapper
==================================================== 

[![PyPI version](https://badge.fury.io/py/pdfgeneratorapi.svg)](https://badge.fury.io/py/pdfgeneratorapi)
[![Build Status](https://travis-ci.org/sameerkumar18/pdfgeneratorapi-python.svg?branch=master)](https://travis-ci.org/sameerkumar18/pdfgeneratorapi-python)
[![image](https://img.shields.io/pypi/v/pdfgeneratorapi.svg)](https://pypi.org/project/pdfgeneratorapi/)
[![image](https://img.shields.io/pypi/l/pdfgeneratorapi.svg)](https://pypi.org/project/pdfgeneratorapi/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/sameerkumar18)
[![image](https://img.shields.io/badge/Paypal-Donate-blue.svg)](https://www.paypal.me/sameerkumar18)

With the PDF Generator API your users can easily create and manage different document templates with an easy-to-use browser based document editor and via API.

An API and template builder to generate PDF documents from Your software, from Your data.

You will first need to [register for a PDFGeneratorAPI account](https://pdfgeneratorapi.com/signup) to use this API. It's free to sign up, and use for testing and integration process.


Installation
------------

Supports Python 3+
To install, simply use pip
```
$ sudo pip install pdfgeneratorapi
✨🍰✨
```

Usage
-----

```python

>>> from pdfgeneratorapi import PDFGenerator

>>> pdf_client = PDFGenerator(api_key='<PDF_GENERATOR_KEY>', api_secret='<PDF_GENERATOR_SECRET>')
>>> pdf_client.set_workspace('<PDF_GENERATOR_WORKSPACE>')
```


You can pass the `api_key`, `api_secret` and `workspace` explicitly. Alternatively, declare these environment variables `PDF_GENERATOR_KEY`, `PDF_GENERATOR_SECRET`.

For wrapper usage code snippets please check examples.py

#### Features


```python

>>> from pdfgeneratorapi import PDFGenerator
>>> pdf_client = PDFGenerator(api_key='<PDF_GENERATOR_KEY>', api_secret='<PDF_GENERATOR_SECRET>')
>>> pdf_client.set_workspace('<PDF_GENERATOR_WORKSPACE>')
```

##### Generate a new Document
```python
>>> new_pdf = pdf_client.create_document(template_id=48484, data={"name": "Sameer Kumar"}, document_format="pdf", response_format="url")
>>> new_pdf.response
'https://us1.pdfgeneratorapi.com/share/5434/ce2fc41de8e51fc7db2cbc1700075a92'
```
##### Fetch All Templates
```python
>>> templates = pdf_client.all_templates(tags=['test_tag'], access=['private'])
>>> templates[0].id
1234
>>> templates[0].name
'Some name'
```
##### Get template by ID
```python
>>> template = pdf_client.get_template(template_id=<TEMPLATE_ID>)
>>> template.layout.format
'A4'
```
##### Create a new template
```python
>>> new_template = pdf_client.create_template(name='<TEMPLATE_NAME>')
>>> new_template.id
24386
>>> new_template.name
'My new template'
```
##### Create a copy of a given template
```python
>>> copy_template = pdf_client.create_template_copy(template_id=48484, name="Copied template")
>>> copy_template.layout.format
'A4'
```
##### Get a one-click link to  web editor
```python
>>> editor_url = pdf_client.get_editor_url(template_id=48484, data={"name": "Sameer"})
'https://us1.pdfgeneratorapi.com/api/v3/templates/19375/editor?key=61e5f04ca1794253ed17e6bb986c1702&workspace=demo.example@actualreports.com&signature=75d7c8fb0c06942da2bf76422f1a79eb72cada6d7ab07f7a7d0eaf8d510897d9&data=https://myawesomeapp.com/data/9129381823.json'
```

Tests
-----
Set the following environment variable:
1. `PDF_GENERATOR_KEY`
2. `PDF_GENERATOR_SECRET`
3. `PDF_GENERATOR_WORKSPACE`

Run the test with the following command:

```
$ python setup.py test
```

## Default Values

You can explicitly override certain default assumptions like - 
- Authentication: Signature Authentication. To use Simple Authentication, simple pass `signature_auth=False` in the object init.
- API URL: `https://<REGION>.pdfgeneratorapi.com/api/<API_VERSION>/` . To override - `api_url='<SOME_URL>'`.
- API Key: `api_key`. Default loads from environment var `PDF_GENERATOR_KEY`
- API Secret: `api_secret`. Default loads from environment var `PDF_GENERATOR_SECRET`
- Workspace: `workspace`. Default loads from environment var `PDF_GENERATOR_WORKSPACE`
- API Region: `api_region`. Default - "us1"
- API Version: `api_version`. Default - "v3"
- Document Format: `document_format`. Default - "pdf"
- Response Format: `response_format`. Default - "base64"

## Documentation

Please see [https://docs.pdfgeneratorapi.com/](https://docs.pdfgeneratorapi.com/) for complete up-to-date documentation.

## About PDFGeneratorAPI.com

PDF Generator API is a RESTful API and a template builder for creating PDF documents from Your software, from Your data. With PDF Generator API you can allow your users to create and manage different document templates with an easy-to-use browser based document editor. And you can merge templates with data from your own software via RESTful API to generate PDF and HTML documents.

## Support
If you have any API related query/issue please contact support@pdfgeneratorapi.com

For any wrapper related query/issue, please raise a GitHub issue.
## About Author
[Sameer Kumar](https://www.sameerkumar.website/)

Find me on [Twitter](https://twitter.com/sameer_kumar018)
