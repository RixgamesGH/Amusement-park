class Settings:

    def __init__(self):
        self.park_name = "Amusement Park"

        self.bg_color = (3, 16, 45)
        self.button_color = (46, 169, 231)
        self.button_txt_color = (0, 0, 0)
        self.text_color = (19, 194, 148)
        self.N_width = 160
        self.N_height = 150

        # Pricing of tickets
        self.babies = 0
        self.kids = 5
        self.adults = 10
        self.elderly = 8
        self.parking_ticket = 7.50

        # Discount for larger groups
        self.minimum_groupsize_discount = 5
        self.discount = 5
