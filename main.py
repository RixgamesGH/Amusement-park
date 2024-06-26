import pygame
from printer import Printer
from settings import Settings
from change_settings import ChangeSettings
from button import Button
from text_box import TextBox
from txt_display import TextDisplay
from price_stats import PriceStats
from generator import Generator
from backend import *
from msg import Msg
import sys


class Main:
    """Overall class to manage assets and behaviour"""
    def __init__(self):
        """Initialize program and create resources"""
        pygame.init()

        # Initialize the printer first to make sure Adobe is installed
        self.printer = Printer()

        # Set up a clock we'll use for the loop
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.change_settings = ChangeSettings(self)

        # Making the program run on full-screen.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()

        # Initialize assets
        self.stats = PriceStats(self)
        self.generator = Generator(self)

        # Define buttons and their positions
        self.B_one = Button(self, 550, -250)
        self.B_two = Button(self, 275, -250)
        self.B_three = Button(self, 0, -250)
        self.B_four = Button(self, -275, -250)
        self.B_five = Button(self, -550, -250)
        self.B_multiselect = Button(self, -0, -150, width=333)
        self.B_corner = Button(self, 750, 450)

        # Define the (number) buttons for custom amount selection
        self.N_1 = Button(self, 185, 185,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_2 = Button(self, 0, 185,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_3 = Button(self, -185, 185,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_4 = Button(self, 185, 0,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_5 = Button(self, 0, 0,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_6 = Button(self, -185, 0,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_7 = Button(self, 185, -185,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_8 = Button(self, 0, -185,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_9 = Button(self, -185, -185,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_0 = Button(self, 0, -370,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_enter = Button(self, -185, -370,
                              width=self.settings.N_width, height=self.settings.N_height)
        self.N_cancel = Button(self, 185, -370,
                               width=self.settings.N_width, height=self.settings.N_height)

        # Initialize the text display resources
        self.msg = Msg("en")
        self.text_box = TextBox(self)
        self.amount_txt = ''
        self.txt = TextDisplay(self)

        # Assets for checking pin for staff access
        self.staff = False
        self.pin_check = False
        self.wrong_pin = False
        self.cashier = False

        # Define the steps and set step 0 on active, rest inactive
        self.step0 = True
        self.step1 = False
        self.custom_number = False
        self.cancel = False
        self.step2 = False
        self.step3 = False
        self.step4 = False
        self.step5 = False
        self.step6 = False
        self.step7 = False
        self.parking_ticket_selection = False
        self.loading = False
        self.saving_receipt = False
        self.multiselect = 1

    def run_program(self):
        """Start the main loop for the program"""
        while True:
            self._check_events()
            self._update_screen()

            if self.loading:
                self._next_step()
                self.loading = False
                pygame.event.clear()
            elif self.saving_receipt:
                self._next_step()
                self.saving_receipt = False
                pygame.event.clear()
            elif self.step7:
                pygame.time.wait(5000)
                self._next_step()
            elif self.wrong_pin:
                pygame.time.wait(2000)
                self._next_step()

            self.clock.tick(60)

    def _check_events(self):
        """Respond to mouse movement and clicks"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                self._check_buttons(mouse_pos)
            elif event.type == pygame.FINGERDOWN:
                finger_pos = event.pos
                self._check_buttons(finger_pos)
            elif event.type == pygame.KEYDOWN:
                if self.custom_number:
                    if event.key == pygame.K_RETURN:
                        self.amount = int(self.amount_txt)
                        self.custom_number = False
                        self._next_step()
                    elif event.key == pygame.K_BACKSPACE:
                        self.amount_txt = self.amount_txt[:-1]
                    else:
                        self.amount_txt += event.unicode
                        try:
                            self.amount_txt = int(self.amount_txt)
                        except ValueError:
                            self.amount_txt = self.amount_txt[:-1]
                        self.amount_txt = str(self.amount_txt)

    def _hover_text(self, button, mouse_pos):
        """Make it so when you hover over the button the text color changes"""
        if button.rect.collidepoint(mouse_pos) and not self.loading and not self.saving_receipt:
            button.button_txt_color = (128, 128, 128)
        else:
            button.button_txt_color = self.settings.button_txt_color

    def _draw_buttons_and_text(self):
        """Draw button selection and text on screen"""
        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        if not self.custom_number:
            # Make the text color change when you hover over a button
            self._hover_text(self.B_one, mouse_pos)
            self._hover_text(self.B_two, mouse_pos)
            self._hover_text(self.B_three, mouse_pos)
            self._hover_text(self.B_four, mouse_pos)
            self._hover_text(self.B_five, mouse_pos)
            self._hover_text(self.B_multiselect, mouse_pos)
            self._hover_text(self.B_corner, mouse_pos)

            if self.step0:
                # Draw buttons for language selection
                self.B_one.draw_button("Nederlands")
                self.B_two.draw_button("English")
                self.B_four.draw_button("Français")
                self.B_five.draw_button("Deutsch")
                self.B_corner.draw_button("Staff only")

            elif self.staff:
                self.B_corner.draw_button("Return")
                self.B_two.draw_button("Close app")
                self.B_three.draw_button("Settings")
                self.B_four.draw_button("Cashier interphase")

            elif self.wrong_pin:
                self.txt.text("That's the wrong PIN")

            elif self.step1:
                # Draw buttons for first selection screen
                self.B_one.draw_button(self.msg.one)
                self.B_two.draw_button(self.msg.two)
                self.B_three.draw_button(self.msg.three)
                self.B_four.draw_button(self.msg.four)
                self.B_five.draw_button(self.msg.five)
                self.B_corner.draw_button(self.msg.return_page)

                # Draw the question on the screen.
                self.txt.text(self.msg.string1)

            elif self.step2:
                # Draw buttons for second selection screen
                self.B_one.draw_button(self.msg.age1)
                self.B_two.draw_button(self.msg.age2)
                self.B_four.draw_button(self.msg.age3)
                self.B_five.draw_button(self.msg.age4)
                self.B_multiselect.draw_button(self.msg.multi.format(x=self.multiselect))
                self.B_corner.draw_button(self.msg.return_page)

                # Draw the question on the screen.
                if self.first_person:
                    amount = self.amount
                    self.person = []
                    while amount != 0:
                        self.person.append(amount)
                        amount -= 1
                    self.first_person = False

                self.txt.text(self.msg.string2.format(x=len(self.person)))

                # Draw the total price at the bottom of the screen
                self.txt.show_price()

                # Show how many of each age group you have selected already under the buttons
                self.txt.text(f"{self.stats.age1}", 550, -325)
                self.txt.text(f"{self.stats.age2}", 275, -325)
                self.txt.text(f"{self.stats.age3}", -275, -325)
                self.txt.text(f"{self.stats.age4}", -550, -325)

            elif self.step3:
                # Draw buttons for third selection screen.
                self.B_two.draw_button(self.msg.yes)
                self.B_four.draw_button(self.msg.no)

                # Draw the question on the screen.
                self.txt.text(self.msg.total1.format(x=self.stats.age1), y=300)
                self.txt.text(self.msg.total2.format(x=self.stats.age2), y=240)
                self.txt.text(self.msg.total3.format(x=self.stats.age3), y=180)
                self.txt.text(self.msg.total4.format(x=self.stats.age4), y=120)
                if self.stats.total_people >= 5:
                    discount = self.msg.yes
                else:
                    discount = self.msg.no
                self.txt.text(self.msg.discount.format(x=discount), y=60)
                self.txt.text(self.msg.string3, y=-60)

                self.txt.show_price()

            elif self.step4 and not self.parking_ticket_selection:
                # Draw buttons for fourth selection screen.
                self.B_two.draw_button(self.msg.yes)
                self.B_three.draw_button(self.msg.multiple)
                self.B_four.draw_button(self.msg.no)
                self.B_corner.draw_button(self.msg.return_page)

                # Draw the question on the screen.
                self.txt.text(self.msg.string4.format(x=self.settings.parking_ticket))
                self.txt.show_price()

            elif self.step4 and self.parking_ticket_selection:
                self._custom_number_selection(mouse_pos)

            elif self.step5:
                # Draw buttons for fifth selection
                self.B_two.draw_button(self.msg.cancel)
                self.B_four.draw_button(self.msg.pay)

                # Draw the text for this step.
                self.txt.text(self.msg.string5.format(x=self.stats.price_total))

            elif self.step6:
                # Draw buttons for sixth screen
                self.B_two.draw_button(self.msg.yes)
                self.B_four.draw_button(self.msg.no)

                # Draw the text for this ste
                self.txt.text(self.msg.string6)

            elif self.step7:
                self.txt.text(self.msg.string7)

        if self.custom_number:
            self._custom_number_selection(mouse_pos)

    def _check_buttons(self, mouse_pos):
        """Check for clicks on the buttons and start the next step"""

        # Check for button clicks
        click_one = self.B_one.rect.collidepoint(mouse_pos)
        click_two = self.B_two.rect.collidepoint(mouse_pos)
        click_three = self.B_three.rect.collidepoint(mouse_pos)
        click_four = self.B_four.rect.collidepoint(mouse_pos)
        click_five = self.B_five.rect.collidepoint(mouse_pos)
        click_multiselect = self.B_multiselect.rect.collidepoint(mouse_pos)
        click_corner = self.B_corner.rect.collidepoint(mouse_pos)

        if not self.custom_number:
            if self.step0:
                if click_one:
                    self.msg = Msg("nl")
                    self._next_step()
                if click_two:
                    self.msg = Msg("en")
                    self._next_step()
                if click_five:
                    self.msg = Msg("de")
                    self._next_step()
                if click_four:
                    self.msg = Msg("fr")
                    self._next_step()
                if click_corner:
                    self.pin_check = True
                    self.custom_number = True

            elif self.staff:
                if click_corner:
                    self.step0 = True
                    self.staff = False
                if click_two:
                    pygame.quit()
                    sys.exit()
                if click_three:
                    self.change_settings.run()
                if click_four:
                    self.cashier = True
                    self.staff = False
                    self.step1 = True

            elif self.step1:
                # Go to next page and assign the amount of people
                if click_one:
                    self.amount = 1
                    self._next_step()

                if click_two:
                    self.amount = 2
                    self._next_step()

                if click_three:
                    self.amount = 3
                    self._next_step()

                if click_four:
                    self.amount = 4
                    self._next_step()

                if click_five:
                    self.custom_number = True

                if click_corner:
                    self.step1 = False
                    self.step0 = True

            elif self.step2:
                # Select the age per person and get the price
                if click_one:
                    self.stats.age1 += self.multiselect
                    self.stats.price_total += self.settings.babies * self.multiselect
                    self._next_step()

                if click_two:
                    self.stats.age2 += self.multiselect
                    self.stats.price_total += self.settings.kids * self.multiselect
                    self._next_step()

                if click_four:
                    self.stats.age3 += self.multiselect
                    self.stats.price_total += self.settings.adults * self.multiselect
                    self._next_step()

                if click_five:
                    self.stats.age4 += self.multiselect
                    self.stats.price_total += self.settings.elderly * self.multiselect
                    self._next_step()

                if click_corner:
                    self.step2 = False
                    self.step1 = True

                if click_multiselect:
                    if self.multiselect == 1 and len(self.person) >= 5:
                        self.B_multiselect.button_color = (21, 131, 186)
                        self.multiselect = 5
                    elif self.multiselect == 5 and len(self.person) >= 10:
                        self.B_multiselect.button_color = (14, 87, 124)
                        self.multiselect = 10
                    elif self.multiselect == 10 and len(self.person) >= 50:
                        self.B_multiselect.button_color = (7, 43, 62)
                        self.multiselect = 50
                    else:
                        self.B_multiselect.button_color = self.settings.button_color
                        self.multiselect = 1

            elif self.step3:
                # Select whether the made selection is correct or not.
                if click_two:
                    self._next_step()
                if click_four:
                    self.step1 = True
                    self.step3 = False

            elif self.step4:
                if self.parking_ticket_selection:
                    self.stats.parking_tickets = self._check_custom_number_selection(mouse_pos)
                    if not self.parking_ticket_selection:
                        self._next_step()
                elif click_three:
                    self.parking_ticket_selection = True
                elif click_two:
                    self.stats.parking_tickets = 1
                    self._next_step()
                elif click_four:
                    self._next_step()
                elif click_corner:
                    self.step3 = True
                    self.step4 = False

            elif self.step5:
                # Clicking on cancel will reset the program and start you at the front
                if click_two:
                    self.step1 = True
                    self.step5 = False
                if click_four:
                    self.loading = True

            elif self.step6:
                if click_two:
                    self.stats.print_receipt = True
                    self.saving_receipt = True
                if click_four:
                    self.stats.print_receipt = False
                    self.saving_receipt = True

        # Run selection for larger groups
        if self.custom_number:
            if self.step0:
                self.staff_pin = self._check_custom_number_selection(mouse_pos)
            if self.step1:
                self.amount = self._check_custom_number_selection(mouse_pos)
            if not self.custom_number and not self.cancel:
                self._next_step()

        pygame.event.clear()

    def _custom_number_selection(self, mouse_pos):
        """Make a menu for selecting a custom amount"""
        # Draw the buttons for the custom selection
        self.N_1.draw_button("1")
        self.N_2.draw_button("2")
        self.N_3.draw_button("3")
        self.N_4.draw_button("4")
        self.N_5.draw_button("5")
        self.N_6.draw_button("6")
        self.N_7.draw_button("7")
        self.N_8.draw_button("8")
        self.N_9.draw_button("9")
        self.N_0.draw_button("0")
        self.N_enter.draw_button(self.msg.enter)
        if not self.amount_txt:
            self.N_cancel.draw_button(self.msg.cancel)
        else:
            self.N_cancel.draw_button(self.msg.remove)

        # Make the text color change when you hover over a button
        self._hover_text(self.N_1, mouse_pos)
        self._hover_text(self.N_2, mouse_pos)
        self._hover_text(self.N_3, mouse_pos)
        self._hover_text(self.N_4, mouse_pos)
        self._hover_text(self.N_5, mouse_pos)
        self._hover_text(self.N_6, mouse_pos)
        self._hover_text(self.N_7, mouse_pos)
        self._hover_text(self.N_8, mouse_pos)
        self._hover_text(self.N_9, mouse_pos)
        self._hover_text(self.N_0, mouse_pos)
        self._hover_text(self.N_enter, mouse_pos)
        self._hover_text(self.N_cancel, mouse_pos)

    def _check_custom_number_selection(self, mouse_pos):
        """Check if a button from the custom number selection is clicked"""
        click_n1 = self.N_1.rect.collidepoint(mouse_pos)
        click_n2 = self.N_2.rect.collidepoint(mouse_pos)
        click_n3 = self.N_3.rect.collidepoint(mouse_pos)
        click_n4 = self.N_4.rect.collidepoint(mouse_pos)
        click_n5 = self.N_5.rect.collidepoint(mouse_pos)
        click_n6 = self.N_6.rect.collidepoint(mouse_pos)
        click_n7 = self.N_7.rect.collidepoint(mouse_pos)
        click_n8 = self.N_8.rect.collidepoint(mouse_pos)
        click_n9 = self.N_9.rect.collidepoint(mouse_pos)
        click_n0 = self.N_0.rect.collidepoint(mouse_pos)
        click_enter = self.N_enter.rect.collidepoint(mouse_pos)
        click_cancel = self.N_cancel.rect.collidepoint(mouse_pos)

        if click_n1:
            self.amount_txt += "1"
        if click_n2:
            self.amount_txt += "2"
        if click_n3:
            self.amount_txt += "3"
        if click_n4:
            self.amount_txt += "4"
        if click_n5:
            self.amount_txt += "5"
        if click_n6:
            self.amount_txt += "6"
        if click_n7:
            self.amount_txt += "7"
        if click_n8:
            self.amount_txt += "8"
        if click_n9:
            self.amount_txt += "9"
        if click_n0:
            self.amount_txt += "0"
        if click_enter:
            try:
                number = int(self.amount_txt)
                self.amount_txt = ""
                if number:
                    self.custom_number = False
                    self.parking_ticket_selection = False
                    self.cancel = False
                    return number
            except ValueError:
                pass
        if click_cancel:
            if not self.amount_txt:
                self.amount_txt = ""
                if self.custom_number:
                    self.custom_number = False
                    self.pin_check = False
                    self.cancel = True
                if self.parking_ticket_selection:
                    self.parking_ticket_selection = False
                    self.step4 = True
            else:
                self.amount_txt = self.amount_txt[:-1]

    def _next_step(self):
        if self.step0:
            self.step0 = False
            if self.pin_check:
                if self.staff_pin == self.settings.password:
                    self.staff = True
                else:
                    self.wrong_pin = True
                self.pin_check = False
            else:
                self.step1 = True

        elif self.wrong_pin:
            self.wrong_pin = False
            self.step0 = True

        elif self.step1:
            self.stats.reset_stats()
            self.txt.prep_price_total()
            self.stats.total_people = self.amount
            self.first_person = True
            self.step1 = False
            self.step2 = True

        elif self.step2:
            try:
                for _ in range(self.multiselect):
                    self.person.pop()
            except IndexError:
                pass
            self.amount -= self.multiselect

            if len(self.person) < 50 and self.multiselect == 50:
                self.B_multiselect.button_color = (14, 87, 124)
                self.multiselect = 10
            if len(self.person) < 10 and self.multiselect == 10:
                self.B_multiselect.button_color = (21, 131, 186)
                self.multiselect = 5
            if len(self.person) < 5:
                self.B_multiselect.button_color = self.settings.button_color
                self.multiselect = 1

            if self.amount == 0:
                if self.stats.total_people >= self.settings.minimum_groupsize_discount:
                    self.stats.price_total -= self.settings.discount
                    if self.stats.price_total < 0:
                        self.stats.price_total = 0
                else:
                    pass

                self.step2 = False
                self.step3 = True

            self.txt.prep_price_total()

        elif self.step3:
            self.step3 = False
            self.step4 = True

        elif self.step4:
            self.stats.price_total += int(self.stats.parking_tickets) * self.settings.parking_ticket
            self.step4 = False
            self.step5 = True

        elif self.step5:
            self.generator.generate_tickets()
            if self.stats.parking_tickets:
                self.generator.generate_parking_tickets()

            self.step5 = False
            self.step6 = True

        elif self.step6:
            self.generator.generate_receipt()
            move_files_to_dir()

            self.step6 = False
            if self.cashier:
                self.step1 = True
            else:
                self.step7 = True

        elif self.step7:
            self.step7 = False
            self.step0 = True

    def _update_screen(self):
        """This will draw the objects on the screen"""
        self.screen.fill(self.settings.bg_color)
        if self.custom_number or self.parking_ticket_selection:
            self.text_box.draw_textbox(self.amount_txt)
        if self.loading:
            self.txt.text(f"{self.msg.loading}...", -275, -350)
            self.B_four.button_txt_color = self.settings.button_txt_color
        if self.saving_receipt:
            if self.stats.print_receipt:
                self.txt.text(f"{self.msg.loading}...", 275, -350)
                self.B_two.button_txt_color = self.settings.button_txt_color
            else:
                self.txt.text(f"{self.msg.saving}...", -275, -350)
                self.B_four.button_txt_color = self.settings.button_txt_color
        self._draw_buttons_and_text()

        pygame.display.flip()


if __name__ == '__main__':
    # Make an instance and run the program
    main = Main()
    main.run_program()
