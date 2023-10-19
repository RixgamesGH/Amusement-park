class Settings:

    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 255)
        self.textbox_color = (255, 255, 255)
        self.N_width = 125
        self.N_height = 120

        # Pricing of tickets
        self.babies = 0
        self.kids = 5
        self.adults = 10
        self.elderly = 8
        self.parking_ticket = 7.50

        # Discount for larger groups
        self.minimum_groupsize_discount = 5
        self.discount = 5
