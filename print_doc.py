from docx import Document
from docx.shared import Inches
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn


class PrintDoc:

    def __init__(self, ap):
        """Make the base of the Word document to print"""
        self.stats = ap.stats
        self.doc = Document()

        # Now Add below children to root xml tree
        # create xml element using OxmlElement
        shd = OxmlElement('w:background')
        # Add attributes to the xml element
        shd.set(qn('w:color'), "#1F2633")  # black color
        # Add background element at the start of Document.xml using below
        self.doc.element.insert(0, shd)
        # Add displayBackgroundShape element to setting.xml
        shd1 = OxmlElement('w:displayBackgroundShape')
        self.doc.settings.element.insert(0, shd1)

        section = self.doc.sections[0]
        section.footer_distance = Inches(0.5)  # Adjust as needed
        section.header_distance = Inches(0.5)  # Adjust as needed
        section.left_margin = Inches(0.5)  # Adjust as needed
        section.right_margin = Inches(0.5)  # Adjust as needed

    def add_ticket(self, ticket):
        self.stats.image_paths += [ticket]  # Replace with your image paths

    def print_doc(self, doc_id):
        for image_path in self.stats.image_paths:
            self.doc.add_picture(image_path, width=Inches(7.5))  # Adjust the size as needed

        # Save the document
        self.doc.save(f"checkout_tickets{doc_id - 1}.docx")
