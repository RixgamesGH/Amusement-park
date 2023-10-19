import pygame.font


class TextDisplay:
    """Class displaying the needed text columns (questions, price, etc.)"""

    def __init__(self, ap):
        """Initialize assets"""
        self.screen = ap.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ap.settings
        self.stats = ap.stats

        # Font settings
        self.text_color = self.settings.text_color
        self.font = pygame.font.SysFont(None, 52)

        self.prep_price_total()

    def prep_price_total(self):
        """Turn the total price in a rendered image"""
        rounded_price = float(round(self.stats.price_total, 2))
        price_str = f"Price total: €{rounded_price:.2f}"
        self.price_image = self.font.render(price_str, True,
                                            self.text_color, self.settings.bg_color)

        # Display the price at the bottom of the screen.
        self.price_rect = self.price_image.get_rect()
        self.price_rect.midbottom = self.screen_rect.midbottom
        self.price_rect.y -= 75

    def show_price(self):
        """Draws price to the screen"""
        self.screen.blit(self.price_image, self.price_rect)

    def text(self, msg, x=0, y=0):
        msg_str = f"{msg}"
        self.text_image = self.font.render(msg_str, True,
                                               self.text_color, self.settings.bg_color)

        # Display the text on the screen
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.screen_rect.center
        self.text_rect.y -= y
        self.text_rect.x -= x

        self.screen.blit(self.text_image, self.text_rect)
