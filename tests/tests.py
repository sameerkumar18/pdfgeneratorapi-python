import json
import os
import unittest

from pdfgeneratorapi import PDFGenerator
from pdfgeneratorapi.decorators import make_response


class TestCase(unittest.TestCase):
    def setUp(self):
        self.pgi = PDFGenerator()

    def prepare_response(self, fixture_name):
        fixture = self._load_fixture(fixture_name)
        fixture_dict = json.loads(fixture)
        return make_response(fixture_dict)

    def _load_fixture(self, name, format="json"):
        with open(
            os.path.dirname(__file__) + "/fixtures/%s.%s" % (name, format), "rb"
        ) as f:
            return f.read()


class PDFGeneratorAPITests(TestCase):
    def test_get_all_templates(self):
        all_templates = self.pgi.templates.all()
        response = self.prepare_response(fixture_name="all_templates")
        self.assertEqual(all_templates, response)

    def test_get_template_by_id(self):
        template = self.pgi.templates.get(template_id=123456)
        response = self.prepare_response(fixture_name="single_template")
        self.assertEqual(template, response)

    def test_create_new_template(self):
        new_template = self.pgi.create_template(name="My new template")
        response = self.prepare_response(fixture_name="create_template")
        self.assertEqual(new_template, response)

    def test_create_template_copy(self):
        copy_template = self.pgi.create_template_copy(
            template_id=24387, name="Copied template"
        )
        response = self.prepare_response(fixture_name="copy_template")
        self.assertEqual(copy_template, response)

    def test_delete_template(self):
        deleted_template = self.pgi.delete_template(template_id=123456)
        response = self.prepare_response(fixture_name="delete_template")
        self.assertEqual(deleted_template, response)

    def test_editor_url(self):
        url = self.pgi.get_editor_url(template_id=48484, data={"name": "Sameer"})
        self.assertTrue(url)


obj = PDFGeneratorAPITests()
obj.test_get_all_templates()
