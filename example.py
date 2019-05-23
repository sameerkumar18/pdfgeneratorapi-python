from pdfgeneratorapi import PDFGenerator

# pdfgen_client = PDFGeneratorAPI()
# print('see this', PDFGeneratorAPI.templates.all())
obj = PDFGenerator()
# obj.all_templates()
print(obj.get_template(template_id=48484))
# # Template testing

# # List of APIs
# """
# Get All Templates
# Get Template by ID
# Create Document
# Create Template
# Copy Template
# Delete Template

# """
# Get All Templates
all_templates = obj.all_templates()
print(all_templates)

# Get Template by ID
template = obj.get_template(template_id=48484)
print(template.id)

# # Create Template
from uuid import uuid4

new_template = obj.create_template(name=str(uuid4()))
print(new_template)

# Copy Template
copy_template = obj.create_template_copy(template_id=48484, name="Copied template")
print(copy_template)

# Delete Template

# Open Editor
link = obj.get_editor_url(template_id=48484, data={"name": "Sameer"})
print(link)

# Create Document
new_pdf = obj.create_document(
    template_id=48484,
    data={"name": "Sameer Kumar"},
    document_format="pdf",
    response_format="url",
)
print(new_pdf.to_dict)
