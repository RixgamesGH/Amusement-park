from pathlib import Path
import json


class PriceStats:
    """Track current total price for the group"""
    def __init__(self, ap):
        """Initialize statistics"""
        self.settings = ap.settings
        self.reset_stats()

        # Ticket ID should never be reset as every tickets needs to have a unique ID
        try:
            path = Path('id_tickets.json')
            contents = path.read_text()
            self.ticket_id = json.loads(contents)
        except FileNotFoundError:
            self.ticket_id = 1

        # This is also the case for parking tickets
        try:
            path = Path('id_parking_tickets.json')
            contents = path.read_text()
            self.parking_ticket_id = json.loads(contents)
        except FileNotFoundError:
            self.parking_ticket_id = 1

    def reset_stats(self):
        """Initialize the price when starting a new selection"""
        self.price_total = 0
        self.agegroup = []
        self.age1 = 0
        self.age2 = 0
        self.age3 = 0
        self.age4 = 0
        self.image_paths = []
