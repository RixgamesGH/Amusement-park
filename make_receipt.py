from jinja2 import Template
from docx import Document
from docx.shared import Pt


class Receipt:

    def __init__(self, ap):
        self.items = {}
        self.stats = ap.stats
        self.settings = ap.settings

    def make_receipt(self):
        if self.stats.age1 != 0:
            self.items[f"{self.stats.age1}x Ticket Baby (age 0-3)"] = \
                float(f"{self.settings.babies * self.stats.age1}")
        if self.stats.age2 != 0:
            self.items[f"{self.stats.age2}x Ticket Kid (age 4-18)"] = \
                float(f"{self.settings.kids * self.stats.age2}")
        if self.stats.age3 != 0:
            self.items[f"{self.stats.age3}x Ticket Adult (age 19-64)"] = \
                float(f"{self.settings.adults * self.stats.age3}")
        if self.stats.age4 != 0:
            self.items[f"{self.stats.age4}x Ticket Elderly (age 65+)"] = \
                float(f"{self.settings.elderly * self.stats.age4}")
        if self.stats.parking_tickets != 0:
            self.items[f"{self.stats.parking_tickets}x Ticket Parking"] = \
                float(f"{self.settings.parking_ticket * self.stats.parking_tickets}")
        if len(self.stats.agegroups) >= 5:
            self.items["Group discount"] = float(f"{self.settings.discount * -1}")

        receipt_text = self._generate_receipt_template()
        self._save_receipt_to_docx(receipt_text)

    def _generate_receipt_template(self):
        template_str = """
{%- for item, price in items.items() %}
{{ item }}:
                                                          €{{ '%0.2f' % price|round(2) }}
{% endfor %}
---------------------------------------------------
Total:                                               €{{ '%0.2f' % total|round(2) }}
"""

        template = Template(template_str)

        total = sum(self.items.values())

        return template.render(items=self.items, total=total)

    def _save_receipt_to_docx(self, receipt_text, page_width=3.5, page_height=4,
                              left_margin=0.5, right_margin=0, top_margin=0.2, bottom_margin=0):
        doc = Document()

        # Set page size
        section = doc.sections[0]
        section.page_width = Pt(page_width * 72)  # Convert inches to points
        section.page_height = Pt(page_height * 72)

        # Set margins
        section.left_margin = Pt(left_margin * 72)
        section.right_margin = Pt(right_margin * 72)
        section.top_margin = Pt(top_margin * 72)
        section.bottom_margin = Pt(bottom_margin * 72)

        doc.add_heading("Receipt Amusement Park", 2)

        # Add receipt content
        text = doc.add_paragraph()
        text.add_run(f"ID{str(self.stats.receipt_id)}\n").font.size = Pt(6)
        text.add_run(receipt_text).font.size = Pt(10)
        text.paragraph_format.line_spacing = Pt(10)

        # Save the document
        filename = f"receipt{self.stats.receipt_id}.docx"
        doc.save(filename)
        print(f"Receipt saved to {filename}")
