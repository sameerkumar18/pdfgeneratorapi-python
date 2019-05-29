# Sample code snippets you can refer for easy copy/paste

from pdfgeneratorapi import PDFGenerator

pdf_client = PDFGenerator(
    api_key="61e5f04ca1794253ed17e6bb986c1702",
    api_secret="68db1902ad1bb26d34b3f597488b9b28",
)
pdf_client.set_workspace("demo.example@actualreports.com")


# For defaults of document_format, response_format, access and other API defaults, please check the `Default Values` section of Readme
# Generate a new Document
new_pdf = pdf_client.create_document(
    template_id=48484,
    data={"name": "Sameer Kumar"},
    document_format="pdf",
    response_format="url",
)

# Fetch All Templates
all_templates = pdf_client.all_templates()
print(all_templates)

# Advanced optional fields =>
# Fetch all templates and filter them by a tag
all_templates = pdf_client.all_templates(tags=["test_tag"])
print(all_templates)

# Fetch all templates and filter them by a access type
all_templates = pdf_client.all_templates(access=["private"])


# Get template info by ID
template = pdf_client.get_template(template_id=48484)

# Create a new template
new_template = pdf_client.create_template(name="some new template")


# Duplicate an existing template
# `name` is optional. You can create a template copy without specifying the name
copy_template = pdf_client.create_template_copy(
    template_id=48484, name="Copied template"
)


# Get a one-click link to  web editor
# Just forms a url
editor_url = pdf_client.get_editor_url(template_id=48484, data={"name": "Sameer"})
