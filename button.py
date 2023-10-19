import pygame


class Button(pygame.sprite.Sprite):
    """Template for the buttons used in the program"""

    def __init__(self, ap, x, y, width=250, height=80):
        """Initialize the assets of the button"""
        super().__init__()

        self.screen = ap.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ap.settings

        self.width, self.height = width, height
        self.button_color = self.settings.button_color
        self.text_color = self.settings.text_color
        self.font = pygame.font.SysFont(None, 40)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Use the x and y values to offset the button from the center
        self.rect.y = self.rect.y - y
        self.rect.x = self.rect.x - x

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, msg):
        self._prep_msg(msg)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
