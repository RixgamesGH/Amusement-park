import pygame
from settings import Settings
from button import Button
from text_box import TextBox
from txt_display import TextDisplay
from price_stats import PriceStats
from make_ticket import Ticket
from print_doc import PrintDoc
from pathlib import Path
import json
import sys
import shutil
import os


class Main:
    """Overall class to manage assets and behaviour"""

    def __init__(self):
        """Initialize program and create resources"""
        pygame.init()

        # Set up a clock we'll use for the loop
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Making the program run on fullscreen.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # Define buttons and their positions
        self.B_one = Button(self, 550, -250)
        self.B_two = Button(self, 275, -250)
        self.B_three = Button(self, 0, -250)
        self.B_four = Button(self, -275, -250)
        self.B_five = Button(self, -550, -250)

        # Define the (number) buttons for custom amount selection
        self.N_1 = Button(self, 150, 150,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_2 = Button(self, 0, 150,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_3 = Button(self, -150, 150,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_4 = Button(self, 150, 0,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_5 = Button(self, 0, 0,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_6 = Button(self, -150, 0,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_7 = Button(self, 150, -150,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_8 = Button(self, 0, -150,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_9 = Button(self, -150, -150,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_0 = Button(self, 0, -300,
                          width=self.settings.N_width, height=self.settings.N_height)
        self.N_enter = Button(self, -150, -300,
                              width=self.settings.N_width, height=self.settings.N_height)
        self.N_cancel = Button(self, 150, -300,
                               width=self.settings.N_width, height=self.settings.N_height)

        # Initialize the text box resources
        self.text_box = TextBox(self)
        self.amount_txt = ''

        # Initialize assets
        self.stats = PriceStats(self)
        self.txt = TextDisplay(self)
        self.doc = PrintDoc(self)

        # Define the steps and set step 1 on active, rest inactive
        self.step1 = True
        self.custom_number = False
        self.step2 = False
        self.step3 = False
        self.step4 = False
        self.step5 = False
        self.parking_ticket_selection = False
        self.parking_tickets = 0

    def run_program(self):
        """Start the main loop for the program"""
        while True:
            self._check_events()
            self._update_screen()
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
        if button.rect.collidepoint(mouse_pos):
            button.text_color = (255, 0, 0)
        else:
            button.text_color = self.settings.text_color

    def _draw_buttons(self):
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

            if self.step1:
                # Draw buttons for first selection screen
                self.B_one.draw_button("One")
                self.B_two.draw_button("Two")
                self.B_three.draw_button("Three")
                self.B_four.draw_button("Four")
                self.B_five.draw_button("Five or more")

                # Draw the question on the screen.
                self.txt.text("With how many people do you want to enter the park?")

            elif self.step2:
                # Draw buttons for second selection screen
                self.B_one.draw_button("0-3 years old")
                self.B_two.draw_button("4-18 years old")
                self.B_four.draw_button("19-64 years old")
                self.B_five.draw_button("65+ years old")

                # Draw the question on the screen.
                if self.first_person:
                    amount = self.amount
                    self.person = []
                    while amount != 0:
                        self.person.append(amount)
                        amount -= 1
                    self.first_person = False

                # Isolate the last number in the list and display the question.
                for x in self.person[-1:]:
                    self.txt.text(f"Under what age-group does person {x} fall?")

                # Draw the total price at the bottom of the screen
                self.txt.show_price()

            elif self.step3:
                # Draw buttons for third selection screen.
                self.B_two.draw_button("Yes")
                self.B_four.draw_button("No")

                # Draw the question on the screen.
                self.txt.text(f"0-3 years old: {self.stats.age1} in total", y=300)
                self.txt.text(f"4-18 years old: {self.stats.age2} in total", y=240)
                self.txt.text(f"19-64 years old: {self.stats.age3} in total", y=180)
                self.txt.text(f"65+ years old: {self.stats.age4} in total", y=120)
                if len(self.stats.agegroup) >= 5:
                    discount = "Yes"
                else:
                    discount = "No"
                self.txt.text(f"Group discount? {discount}", y=60)
                self.txt.text(f"Is this correct?", y=-60)

                self.txt.show_price()

            elif self.step4 and not self.parking_ticket_selection:
                # Draw buttons for fourth selection screen.
                self.B_two.draw_button("Yes")
                self.B_three.draw_button("Yes, multiple")
                self.B_four.draw_button("No")

                # Draw the question on the screen.
                self.txt.text(f"Would you like to buy a parking ticket as well for €"
                              f"{self.settings.parking_ticket:.2f}?")

                self.txt.show_price()

            elif self.step4 and self.parking_ticket_selection:
                self._custom_number_selection(mouse_pos)

            elif self.step5:
                # Draw buttons for fifth selection
                self.B_two.draw_button("Cancel")
                self.B_four.draw_button("Pay")

                # Draw the text for this step.
                self.txt.text(f"Your total will come out to be €{self.stats.price_total:.2f}")

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

        if not self.custom_number:
            if self.step1:
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

            elif self.step2:
                # Select the age per person and get the price
                if click_one:
                    self.stats.agegroup.append(1)
                    self.stats.price_total += self.settings.babies
                    self._next_step()

                if click_two:
                    self.stats.agegroup.append(2)
                    self.stats.price_total += self.settings.kids
                    self._next_step()

                if click_four:
                    self.stats.agegroup.append(3)
                    self.stats.price_total += self.settings.adults
                    self._next_step()

                if click_five:
                    self.stats.agegroup.append(4)
                    self.stats.price_total += self.settings.elderly
                    self._next_step()

            elif self.step3:
                # Select whether the made selection is correct or not.
                if click_two:
                    self._next_step()
                if click_four:
                    self.amount_txt = ""
                    self.step1 = True
                    self.step3 = False

            elif self.step4:
                if self.parking_ticket_selection:
                    self.parking_tickets = self._check_custom_number_selection(mouse_pos)
                    if not self.parking_ticket_selection:
                        self._next_step()
                elif click_three:
                    self.parking_ticket_selection = True
                elif click_two:
                    self.stats.price_total += self.settings.parking_ticket
                    self._next_step()
                elif click_four:
                    self._next_step()

            elif self.step5:
                # Clicking on cancel will reset the program and start you at the front
                if click_two:
                    self.step1 = True
                    self.step5 = False
                if click_four:
                    # Making and printing the tickets on a Word document
                    for _ in range(self.stats.age1):
                        Ticket("Age 0-3", self.settings.babies, self.stats.ticket_id)
                        self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
                        self.stats.ticket_id += 1
                    for _ in range(self.stats.age2):
                        Ticket("Age 4-18", self.settings.kids, self.stats.ticket_id)
                        self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
                        self.stats.ticket_id += 1
                    for _ in range(self.stats.age3):
                        Ticket("Age 19-64", self.settings.adults, self.stats.ticket_id)
                        self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
                        self.stats.ticket_id += 1
                    for _ in range(self.stats.age4):
                        Ticket("Age 65+", self.settings.elderly, self.stats.ticket_id)
                        self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
                        self.stats.ticket_id += 1

                    self.doc.print_doc(self.stats.ticket_id)

                    # Save the ticket ID so each guest gets unique ID's
                    path = Path('id_tickets.json')
                    ticket_id = json.dumps(self.stats.ticket_id)
                    path.write_text(ticket_id)

                    self._move_files_to_dir()

        # Run selection for larger groups
        if self.custom_number:
            self.amount = self._check_custom_number_selection(mouse_pos)

    @staticmethod
    def _move_files_to_dir():
        """Move the files made into their respective directory"""
        source = "C:/Users/Admin/Documents/GitHub/Amusement-park"
        dest1 = "C:/Users/Admin/Documents/GitHub/Amusement-park/ticket_images/"
        dest2 = "C:/Users/Admin/Documents/GitHub/Amusement-park/checkout_doc/"
        files = os.listdir(source)

        for f in files:
            if f.startswith("ticket"):
                shutil.move(f, dest1)
            if f.startswith("checkout"):
                shutil.move(f, dest2)


    def _custom_number_selection(self, mouse_pos):
        """Make a menu for selecting a custom amount"""
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

        # Pull up the menu for custom number selection
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
        self.N_enter.draw_button("enter")
        if not self.amount_txt:
            self.N_cancel.draw_button("cancel")
        else:
            self.N_cancel.draw_button("remove")

    def _check_custom_number_selection(self, mouse_pos):
        # Draw the buttons for the custom selection
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
                if number:
                    if self.custom_number:
                        self.custom_number = False
                        self._next_step()
                    self.parking_ticket_selection = False
                    return number
            except ValueError:
                pass
        if click_cancel:
            if not self.amount_txt:
                self.amount_txt = ""
                if self.custom_number:
                    self.custom_number = False
                    self.step1 = True
                if self.parking_ticket_selection:
                    self.parking_ticket_selection = False
                    self.step4 = True
            else:
                self.amount_txt = self.amount_txt[:-1]

    def _next_step(self):
        if self.step1:
            self.stats.reset_stats()
            self.txt.prep_price_total()
            self.first_person = True
            self.step1 = False
            self.step2 = True

        elif self.step2:
            self.person.pop()
            self.amount -= 1
            if self.amount == 0:
                if len(self.stats.agegroup) >= self.settings.minimum_groupsize_discount:
                    self.stats.price_total -= self.settings.discount
                    if self.stats.price_total < 0:
                        self.stats.price_total = 0
                else:
                    pass
                for x in self.stats.agegroup:
                    if x == 1:
                        self.stats.age1 += 1
                    if x == 2:
                        self.stats.age2 += 1
                    if x == 3:
                        self.stats.age3 += 1
                    if x == 4:
                        self.stats.age4 += 1
                self.step2 = False
                self.step3 = True
            self.txt.prep_price_total()

        elif self.step3:
            self.amount_txt = ""
            self.step3 = False
            self.step4 = True

        elif self.step4:
            self.stats.price_total += int(self.parking_tickets) * self.settings.parking_ticket
            self.step4 = False
            self.step5 = True

    def _update_screen(self):
        """This will draw the objects on the screen"""
        self.screen.fill(self.settings.bg_color)
        if self.custom_number or self.parking_ticket_selection:
            self.text_box.draw_textbox(self.amount_txt)
        self._draw_buttons()

        pygame.display.flip()


if __name__ == '__main__':
    # Make an instance and run the program
    main = Main()
    main.run_program()
