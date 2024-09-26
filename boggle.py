#################################################################
# FILE : boggle.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex11 2022-2023
# DESCRIPTION: The Controller aspect of the Boggle Game
#################################################################
from boggle_logic import BoggleLogic
from boggle_gui import BoggleGui
from boggle_board_randomizer import *
import os

class BoggleController:
    """Boggle Game Controller, links between Gui and Logic
        and runs the Game
    """
    def __init__(self):
        all_word_from_dict =  load_words_dict(file_path("boggle_dict.txt"))

        self.__gui = BoggleGui(self)
        self.__game_logic = BoggleLogic(self,all_word_from_dict)
        
    def run(self):
        """runs window"""
        self.__gui.run()

    def start_game(self):
        """ This function Randomizes a board, sends it to 
            Logic And GUI and starts the game
        """
        board = randomize_board()

        self.__gui.set_board(board)
        self.__game_logic.set_game(board)
                
        self.__gui.start_game()

    def tile_clicked(self,y,x):
        self.__game_logic.tile_clicked(y,x)

    def add_to_word_bank(self,word):
        self.__gui.add_to_word_bank(word)
    
    def clear_board(self):
        self.__gui.clear_board()
    
    def update_score(self,score):
        self.__gui.set_score(score)
        
    def update_word(self,word):
        self.__gui.update_word(word)

#########################################
#extracting words from given txt file (boggle_dict.txt)

def file_path(name):
    return os.path.join(name)

def load_words_dict(file):
    milon = open(file)
    lines = set(line.strip() for line in milon.readlines())
    milon.close()
    return lines
#########################################
if "__main__" == __name__:
    controller = BoggleController()
    controller.run()
        

