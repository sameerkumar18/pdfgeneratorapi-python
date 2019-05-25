import json
import os
from uuid import uuid4
import unittest

from pdfgeneratorapi import PDFGenerator
from pdfgeneratorapi.utils import dict_to_object


class TestCase(unittest.TestCase):
    def setUp(self):
        from dotenv import load_dotenv

        load_dotenv(verbose=True)
        self.pgi = PDFGenerator()
        self.sample_template_id = self.pgi.create_template(name=str(uuid4)).id

    def prepare_response(self, fixture_name):
        fixture = self._load_fixture(fixture_name)
        fixture_dict = json.loads(fixture.decode("utf-8"))
        return dict_to_object(fixture_dict)

    def _load_fixture(self, name, fixture_format="json"):
        with open(
            os.path.dirname(__file__) + "/fixtures/%s.%s" % (name, fixture_format), "rb"
        ) as f:
            return f.read()


class PDFGeneratorAPITests(TestCase):
    def test_get_all_templates(self):
        all_templates = self.pgi.all_templates()
        response = self.prepare_response(fixture_name="all_templates")
        self.assertEqual(type(all_templates), type(response))

    def test_get_template_by_id(self):
        template = self.pgi.get_template(template_id=self.sample_template_id)
        response = self.prepare_response(fixture_name="single_template")
        self.assertEqual(type(template), type(response))
        self.assertEqual(type(template.id), type(response.id))

    def test_create_new_template(self):
        new_template = self.pgi.create_template(name="My new template")
        response = self.prepare_response(fixture_name="create_template")
        self.assertEqual(type(new_template), type(response))
        self.assertEqual(hasattr(new_template, "id"), hasattr(response, "id"))

    def test_create_template_copy(self):
        copy_template = self.pgi.create_template_copy(
            template_id=self.sample_template_id, name="Copied template"
        )
        response = self.prepare_response(fixture_name="copy_template")
        self.assertEqual(type(copy_template), type(response))
        self.assertEqual(hasattr(copy_template, "id"), hasattr(response, "id"))

    def test_remove_template(self):
        deleted_template = self.pgi.delete_template(template_id=self.sample_template_id)
        response = self.prepare_response(fixture_name="delete_template")
        self.assertEqual(type(deleted_template), type(response))
        self.assertEqual(len(deleted_template.to_dict), len(deleted_template.to_dict))

    def test_editor_url(self):
        url = self.pgi.get_editor_url(
            template_id=self.sample_template_id, data={"name": "Sameer"}
        )
        self.assertTrue(url)

    def test_create_document(self):
        response = self.prepare_response(fixture_name="create_document")
        document = self.pgi.create_document(
            template_id=self.sample_template_id, data={"name": "Sameer"}
        )
        self.assertEqual(type(document), type(response))
        self.assertEqual(len(document.to_dict), len(response.to_dict))
