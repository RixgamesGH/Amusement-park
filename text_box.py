import pygame


class TextBox:
    """Text box for inputting numbers for amount of people"""
    def __init__(self, ap, width=425, height=125):
        """Initialize assets for the text box"""
        self.screen = ap.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ap.settings

        self.width, self.height = width, height
        self.textbox_color = self.settings.textbox_color
        self.text_color = self.settings.text_color
        self.font = pygame.font.SysFont(None, 52)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.rect.y = self.rect.y - 325

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.textbox_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_textbox(self, msg):
        self._prep_msg(msg)
        self.screen.fill(self.textbox_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
