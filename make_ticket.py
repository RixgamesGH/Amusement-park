from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime


class Ticket:

    def __init__(self, ticket_type, price, ticket_id):
        """Initialize the assets to make a ticket"""

        self.background_color = (31, 38, 51, 255)
        self.text_color = (139, 189, 127, 255)
        self.text_stroke = (57, 94, 49, 255)
        self.image_outline = (84, 70, 58, 84)
        self.border_color = (60, 52, 54, 200)
        self.outline_color = (132, 160, 124, 130)

        # Create a blank ticket image
        self.width, self.height = 800, 300
        self.ticket = Image.new('RGBA', (self.width, self.height), color=self.background_color)

        # Create a drawing context on the ticket
        self.draw = ImageDraw.Draw(self.ticket)

        # Make a background pattern with a lighter shade than the background
        self.y1 = -260
        self.y2 = -240
        self.y3 = 20
        self.y4 = 0
        self.opacity = 255

        while self.opacity >= 0:
            self.draw.polygon(([(self.y1, 20), (self.y2, 20), (self.y3, 280), (self.y4, 280)]),
                              (86, 96, 118, self.opacity))
            self.y1 += 20
            self.y2 += 20
            self.y3 += 20
            self.y4 += 20
            self.opacity -= 5

        # Load the image for the ticket (replace 'image.jpg' with your image file)
        self.image = Image.open('amusement_park.png')
        self.image = self.image.resize((170, 170))  # Resize the image if needed
        self.ticket.paste(self.image, (580, 76))

        # Create a border around the image
        self.draw.line([(580, 76), (750, 76)], self.image_outline, width=2)
        self.draw.line([(580, 76), (580, 246)], self.image_outline, width=2)
        self.draw.line([(580, 246), (750, 246)], self.image_outline, width=2)
        self.draw.line([(750, 76), (750, 247)], self.image_outline, width=2)

        # Define text and font properties
        self.font = ImageFont.truetype("arial.ttf", 22)
        self.title_font = ImageFont.truetype("arial.ttf", 40)
        self.small_font = ImageFont.truetype("arial.ttf", 12)

        # Create a border around the ticket for aesthetic purposes
        self.border_forms = [
            [(0, 0), (800, 20)],
            [(0, 0), (20, 300)],
            [(0, 280), (800, 300)],
            [(780, 0), (800, 280)],
        ]

        for coords in self.border_forms:
            try:
                self.draw.rectangle(coords, self.border_color)
            except ValueError:
                print(coords)

        # Make outlines highlighting the border.
        self.outline_coords = [
            [(0, 0), (20, 20)],
            [(0, 300), (20, 280)],
            [(780, 20), (800, 0)],
            [(780, 280), (800, 300)],
            [(20, 20), (20, 280)],
            [(20, 280), (780, 280)],
            [(780, 20), (780, 280)],
            [(20, 20), (780, 20)],
            [(0, 0), (800, 0)],
            [(799, 0), (799, 300)],
            [(0, 0), (0, 300)],
            [(0, 299), (800, 299)],
        ]

        for coords in self.outline_coords:
            try:
                self.draw.line(coords, self.outline_color)
            except ValueError:
                print(coords)

        # Get the current date and time
        today = datetime.now()
        date = today.strftime("%B %d, %Y %H:%M")

        # Draw text on the ticket
        self.draw.text((150, 44), "Amusement park", fill=self.text_color,
                       font=self.title_font, stroke_width=1, stroke_fill=self.text_stroke)
        self.draw.text((336, 84), f"{ticket_type}", fill=self.text_color,
                       font=self.title_font, stroke_width=1, stroke_fill=self.text_stroke)
        self.draw.text((220, 170), f"Price: €{price:.2f}", fill=self.text_color, font=self.font)
        self.draw.text((220, 200), f"{date}*", fill=self.text_color, font=self.font)
        self.draw.text((220, 230), f"Ticket ID: {ticket_id}", fill=self.text_color, font=self.font)
        if ticket_type != "Parking ticket":
            self.draw.text((550, 256), "*ticket is valid for 7 days after purchase",
                           fill=self.text_color, font=self.small_font)
        else:
            self.draw.text((550, 256), "*ticket only valid on day of purchase",
                           fill=self.text_color, font=self.small_font)

        # Create a QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=2,
        )

        qr.add_data('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  # Replace with your URL or data
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=(240, 159, 31), back_color=self.background_color)
        self.ticket.paste(qr_img, (36, 138))

        if ticket_type == "Parking ticket":
            self.ticket.save(f"parking_ticket{ticket_id}.png")
        else:
            self.ticket.save(f"ticket{ticket_id}.png")


# Some code, so I can run a test outside the main loop to see how the ticket will look
if __name__ == "__main__":
    run = Ticket("test", 5, "_example")
    run.ticket.show()
