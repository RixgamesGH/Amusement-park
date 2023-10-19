class PriceStats:
    """Track current total price for the group"""
    def __init__(self, ap):
        """Initialize statistics"""
        self.settings = ap.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize the price when starting a new selection"""
        self.price_total = 0
        self.agegroup = []
        self.age1 = 0
        self.age2 = 0
        self.age3 = 0
        self.age4 = 0