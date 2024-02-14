import pygame


class Button(pygame.sprite.Sprite):
    """Template for the buttons used in the program"""

    def __init__(self, main, x, y, width=260, height=80):
        """Initialize the assets of the button"""
        super().__init__()

        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main.settings

        self.width, self.height = width * self.settings.r_width, height * self.settings.r_height
        self.button_color = self.settings.button_color
        self.button_txt_color = self.settings.button_txt_color
        self.font = pygame.font.SysFont(None, 40 * self.settings.r_height)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Use the x and y values to offset the button from the center
        self.rect.y = self.rect.y - y * self.settings.r_height
        self.rect.x = self.rect.x - x * self.settings.r_width

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.button_txt_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, msg):
        self._prep_msg(msg)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
