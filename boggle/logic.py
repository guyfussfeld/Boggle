#################################################################
# FILE : logic.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex11 2022-2023
# DESCRIPTION: The logic aspect of the Boggle Game
#################################################################
from utils import *

class BoggleLogic:
    """The logic behind the game of Boggle"""
    def __init__(self,controller,words) -> None:

        self.__Boggle_Controller = controller

        self.__words = words
        self.__current_word_path: list[tuple] = []
        self.__word_bank: list = []
        self.__boggle_board: list[list[str]] = []
        self.__score: int = 0
        
    def set_game(self,board):
        """this function sets a board, and clears fields,
            preparing a new game of Boggle
        """
        self.__boggle_board = board
        self.__word_bank = []
        self.__current_word_path = []
        self.__score = 0

    def reset_board(self):
        """this function clears current word, and alerts controller"""
        self.__current_word_path = []
        self.__Boggle_Controller.clear_board()

    def _check_word_formed(self):
        """this function checks if the formed word is a new valid word
           and updates controller and word_bank if so."""
        word = is_valid_path(self.__boggle_board,self.__current_word_path,self.__words)
        if word != None: #checks if word exists in board
            if word not in self.__word_bank: #word wasnt found before
                self.word_success()
        #update controller
        self.__Boggle_Controller.update_word(self.get_word())   

    def tile_clicked(self,y,x):
        """this function occurs when a tile is clicked,
            it checks if the tile clicked was in reach, if not, it clears
            the current word and alerts the controller. then it checks if 
            a word was formed, in that case it clears the current word, updates
            word_bank and controller.
        """
        if len(self.__current_word_path) > 0: #not first tile
            if check_step_valid(self.__current_word_path[-1],(y,x))\
                 and (y,x) not in self.__current_word_path: #if legal step
                self.__current_word_path.append((y,x))              
                self._check_word_formed()
            else:
                self.word_failed()
                
        else: #first tile handling
            self.__current_word_path.append((y,x))
            self._check_word_formed()

    def word_success(self):
        """this function deals with the case a word was formed
            alerts controller, updates score, word_bank, current word
            and resets board"""
        word = self.get_word()
        self.__word_bank.append(word)
        self.update_score(len(self.__current_word_path)**2)
        self.__Boggle_Controller.add_to_word_bank(word)
        self.reset_board()

    def word_failed(self):
        """this funtion deals with the case a word building failed.
            clears current word"""
        self.reset_board()

    def get_word(self):
        """return the word current path is representing"""
        return "".join([self.__boggle_board[coord[0]][coord[1]] for coord in self.__current_word_path])
    
    def update_score(self,score):
        """updates score and controller about the score"""
        self.__score += score
        self.__Boggle_Controller.update_score(self.__score)
        
        

    


    
    