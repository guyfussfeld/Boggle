from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]

BOARD_WIDTH = 4
BOARD_HEIGHT = 4


def check_step_valid(coord1,coord2):
    """this function checks if a step between two board tiles is valid"""
    if not _check_in_bounds_(coord2): #coord out of bounds
        return False
    y,x = coord1
    eight_allowed_directions = [(y+1,x-1),(y+1,x),(y+1,x+1),(y,x+1),(y-1,x-1),(y,x-1),(y-1,x),(y-1,x+1)] 
    if coord2 in eight_allowed_directions:
        return True
    return False

def _check_in_bounds_(coord):
    """this function returns True if a given coord is in board else False"""
    return not ((coord[0] < 0 or coord[0] >= BOARD_HEIGHT) or (coord[1] < 0 or coord[1] >= BOARD_WIDTH))
    
def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """this function gets a path of Boggle game, a board, and words
        and returns the path's word if its in words. else returns None
    """
    word = ""

    past_tiles = []

    for i,coord in enumerate(path):
        if coord in past_tiles: #tile used already
            return 
        if not _check_in_bounds_(coord): #coord out of bounds
            return 
        
        word += board[coord[0]][coord[1]]
        if i != len(path)-1: # if not the last path tile
            if not check_step_valid(coord,path[i+1]):
                return 
        past_tiles.append(coord)

    if word in words:
        return word 

def _get_available_next_tiles(current_path):
    """this function gets a path, and returns the next available tiles,
        next tiles must be in reach, new (not it path already), and in board bounds
    """
    current_tile = current_path[-1] #last tile of path 
    y,x = current_tile
    eight_allowed_directions = [(y+1,x-1),(y+1,x),(y+1,x+1),(y,x+1),(y-1,x-1),(y,x-1),(y-1,x),(y-1,x+1)] 
    return [tile for tile in eight_allowed_directions if (tile not in current_path) and (_check_in_bounds_(tile))]

def find_length_n_helper(n: int,current_path,board,words,is_path: bool):
    """this function recursivley builds all legal paths/words of n length 
        of the Boggle Game
    """
    all_paths = []
    word = "".join([board[coord[0]][coord[1]] for coord in current_path])
    if is_path:
        if n == 0: #built an n-length word             
            if word in words:
                return [current_path]
            else:
                return []
    else: #word
        if len(word) >= n:
            if len(word) != n:
                return []
            else:
                if word in words:
                    return [current_path]

    #more tiles to be explored
    available_next_tiles = _get_available_next_tiles(current_path)

    if len(available_next_tiles) == 0: #dead end
        return []
        
    for next_tile in available_next_tiles: # try every possible tile
        if is_path:
            next_find = find_length_n_helper(n-1,current_path+[next_tile],board,words,is_path)
        else:
            next_find = find_length_n_helper(n,current_path+[next_tile],board,words,is_path)

        for path in next_find:
            all_paths.append(path)            
    return all_paths
    
def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """this function returns all legal n-length paths of Boggle Game"""
    length_n_paths = []
    #try all start points
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            new_path_try = find_length_n_helper(n-1,[(i,j)],board,words,True)            
            for path in new_path_try:
                length_n_paths.append(path)
    return length_n_paths

def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """this function returns all legal n-length words of Boggle Game"""
    length_n_words = []
    #try all start points
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            new_path_try = find_length_n_helper(n,[(i,j)],board,words,False)            
            for path in new_path_try:
                length_n_words.append(path)
    return length_n_words

def _max_score_paths_helper(word,current_path,board):    
    """this function backtracks on a Boggle board, finding a max score
        path a given word can produce.
    """
    current_built_word = "".join([board[coord[0]][coord[1]] for coord in current_path])
    
    if word.find(current_built_word) != 0: #wrong path letters dont match
        return []

    all_paths = []

    if current_built_word == word:
        return [current_path]
    else: 
        #more tiles to be explored
        available_next_tiles = _get_available_next_tiles(current_path)

        if len(available_next_tiles) == 0: #dead end
            return []
            
        for next_tile in available_next_tiles: # try every possible tile
            next_find = _max_score_paths_helper(word,current_path+[next_tile],board)

            for path in next_find:
                all_paths.append(path)             
    return all_paths

    

def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """this function backtracks on a Boggle board, finding a max score
        path each word can produce.
    """
    max_score_paths = []
    for word in words:
        paths = []
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                paths += _max_score_paths_helper(word,[(i,j)],board)
        
        if paths:
            max_score_paths.append(max(paths, key=lambda p: len(p)))                    
    return max_score_paths

