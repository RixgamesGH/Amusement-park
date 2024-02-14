from docx import Document
from docx.shared import Inches
from docx2pdf import convert
import os


class PrintDoc:

    def __init__(self):
        """Make the base of the Word document to print"""
        self.image_paths = []

    def add_ticket(self, ticket):
        self.image_paths += [ticket]  # Replace with your image paths

    def print_doc(self, doc_id, ticket_type):
        doc = Document()

        section = doc.sections[0]
        section.left_margin = Inches(0.5)  # Adjust as needed
        section.right_margin = Inches(0.5)  # Adjust as needed

        for image_path in self.image_paths:
            doc.add_picture(image_path, width=Inches(7.5))  # Adjust the size as needed

        # Save the document
        input_file = f"checkout_{ticket_type}{doc_id - 1}.docx"
        doc.save(input_file)
        self.image_paths = []

        # Convert to pdf
        output_file = f"checkout_{ticket_type}{doc_id - 1}.pdf"
        file = open(output_file, "w")
        file.close()
        convert(input_file, output_file)
        os.remove(input_file)
