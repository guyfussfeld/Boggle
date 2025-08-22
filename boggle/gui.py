#################################################################
# FILE : gui.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex11 2022-2023
# DESCRIPTION: The GUI aspect of the Boggle Game
#################################################################
import tkinter as tki
import time


class BoggleGui():
    """The GUI of Boggle Game"""
    GAME_TIME = 180
    DEFAULT_COLOR = "white"
    BOARD_HEIGHT = 4
    BOARD_WIDTH = 4

    def __init__(self, controller):
        self.__boggle_controller = controller
        self.__timer = BoggleGui.GAME_TIME
        self.__is_game_running = False

        # Widgets:
        self.__root = tki.Tk()
        self.__root.configure(bg="gray")
        self.__root.title("Yonatan & Guy's Boggle")
        self.__root.resizable(False, False)
        # Top Left Frame (Time)
        self.__frame1 = tki.LabelFrame(self.__root, width=400, height=50, bd=1)
        self.__frame1.pack_propagate(False)
        self.__frame1.grid(row=0, column=0)

        self.__label1 = tki.Label(
            self.__frame1, text="Time Left: ", borderwidth=0, relief="solid", font=("Ariel", 20))
        self.__label1.pack(side=tki.LEFT, padx=80)

        self.__label2 = tki.Label(
            self.__frame1, text="03:00", borderwidth=0, relief="solid", font=("Ariel", 20))
        self.__label2.pack(side=tki.LEFT, padx=0)
        self.set_time()
        # Top Right Frame (Score)
        self.__frame2 = tki.LabelFrame(self.__root, width=400, height=50, bd=1)
        self.__frame2.pack_propagate(False)
        self.__frame2.grid(row=0, column=1)

        self.__label3 = tki.Label(
            self.__frame2, text="Score: ", borderwidth=0, relief="solid", font=("Ariel", 20))
        self.__label3.pack(side=tki.LEFT, padx=80)

        self.__label4 = tki.Label(
            self.__frame2, text="0", borderwidth=0, relief="solid", font=("Ariel", 20))
        self.__label4.pack(side=tki.LEFT, padx=0)
        # Top-Middle Frame (Current Word)
        self.__frame3 = tki.LabelFrame(self.__root, width=800, height=50, bd=1)
        self.__frame3.pack_propagate(False)
        self.__frame3.grid(row=1, column=0, columnspan=2)

        self.__label6 = tki.Label(
            self.__frame3, text="", borderwidth=0, relief="solid", font=("Ariel", 20))
        self.__label6.pack(pady=8)
        # Left-Center Frame (Tiles)
        self.__mainframe_left = tki.LabelFrame(
            self.__root, width=400, height=400, bd=1)
        self.__mainframe_left.grid(row=2, column=0, columnspan=1)

        self.__buttons: list[list[any]] = []
        for i in range(4):
            button_row = []
            for j in range(4):
                button = tki.Button(self.__mainframe_left, height=3, width=7, font=("Ariel", 15),
                                    command=lambda y=i, x=j: self._tile_button_clicked(y, x), state=tki.DISABLED)
                button.grid(row=i, column=j)
                button_row.append(button)
            self.__buttons.append(button_row)
        # Right-Center Frame (Word Bank)
        self.__mainframe_right = tki.LabelFrame(
            self.__root, width=400, height=400, bd=1)
        self.__mainframe_right.pack_propagate(False)
        self.__mainframe_right.grid(row=2, column=1, columnspan=1)

        self.__list_box = tki.Listbox(
            self.__mainframe_right, state=tki.DISABLED, height=150)
        self.__list_box.pack(side=tki.TOP, pady=50)
        # Bottom Frame (Play Button)
        self.__bottomframe = tki.LabelFrame(
            self.__root, width=800, height=100, bd=1)
        self.__bottomframe.pack_propagate(False)
        self.__bottomframe.grid(row=3, column=0, columnspan=2)

        self.__play_button = tki.Button(self.__bottomframe, text="Play",
                                        command=lambda: self.__boggle_controller.start_game(), padx="20", pady="10", font=("Ariel", 15, "bold"))
        self.__play_button.pack(pady=20)
        ###################################

    def run(self):
        """Runs the tkinter mainloop"""
        self.__root.mainloop()

    def set_board(self, board: list[list[str]]):
        """this function gets a random board from controller, and update tiles text"""
        for i in range(BoggleGui.BOARD_HEIGHT):
            for j in range(BoggleGui.BOARD_WIDTH):
                self.__buttons[i][j].configure(text=board[i][j])
                self.__buttons[i][j].configure(bg=BoggleGui.DEFAULT_COLOR)
        self.update_word("")

    def start_game(self):
        """ starts game: 
        1) resets time and score
        2) clears word bank
        3) enables tiles
        """
        self.__timer = BoggleGui.GAME_TIME

        if not self.__is_game_running:  # start ticking
            self.tick()
        self.__is_game_running = True

        self.set_score(0)
        self.clear_word_bank()
        for button_row in self.__buttons:
            for button in button_row:
                button["state"] = tki.NORMAL

    def game_over(self):
        """this function happens when a game is over, does:
        1) resets time, clears work bank
        2) clears and disable buttons
        3) reset current word
        """
        self.__timer = BoggleGui.GAME_TIME
        self.set_time()

        self.__is_game_running = False

        self.clear_word_bank()

        for button_row in self.__buttons:
            for button in button_row:
                button["state"] = tki.DISABLED
                button["text"] = ""
                button["bg"] = BoggleGui.DEFAULT_COLOR
        self.update_word("")

    def tick(self):
        """ This function ticks every 1 second, updates time label
            and alerts when Game time is over
        """
        self.set_time()
        self.__timer -= 1

        if self.__timer < 0:  # game over
            self.game_over()
        else:
            self.__root.after(1000, self.tick)

    def _tile_button_clicked(self, y, x):
        """Colors button and updates controller"""
        self.__buttons[y][x].configure(bg="Teal")
        self.__boggle_controller.tile_clicked(y, x)

    def switch_widget(self, widget):
        """switches widget state"""
        if widget["state"] == tki.NORMAL:
            widget["state"] = tki.DISABLED
        else:
            widget["state"] = tki.NORMAL

    def _buttons_switch(self):
        """switches buttons state"""
        for button_row in self.__buttons:
            for button in button_row:
                self.switch_widget(button)

    def clear_word_bank(self):
        """clears word bank"""
        self.switch_widget(self.__list_box)
        self.__list_box.delete(0, tki.END)
        self.switch_widget(self.__list_box)

    def set_score(self, score):
        self.__label4.configure(text=score)

    def set_time(self):
        display_time = time.strftime("%M:%S", time.gmtime(self.__timer))
        self.__label2.configure(text=display_time)

    def update_word(self, word):
        self.__label6.configure(text=word)

    def add_to_word_bank(self, word):
        """Add word to word bank"""
        self.switch_widget(self.__list_box)
        self.__list_box.insert(tki.END, word)
        self.switch_widget(self.__list_box)

    def clear_board(self):
        """clears board and current word"""
        for button_row in self.__buttons:
            for button in button_row:
                button.configure(bg=BoggleGui.DEFAULT_COLOR)

        self.update_word("")
