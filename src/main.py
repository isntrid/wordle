from typing import List
def get_words() -> List[str]:
    '''
    This function looks at words.txt, a text file containing hundreds of thousands of words
    and then puts any 5 letter, english words that have no numbers into a list and returns it.
    
    Returns:
        words List[str]: contains a list of every valid word.
        
    Raises:
        FileNotFoundError: No valid word or dictionary of words list was found.
        PermissionError: Program was denied permission to access and read dictionary file.
    '''
    
    try:
        with open("words.txt", 'r') as w:
            lines = w.readlines()
            words = [
                word for w in lines 
                if (word := w.strip().lower()).isalpha() 
                and word.isascii() and len(word) == 5
                ]
    except FileNotFoundError as e:
        raise FileNotFoundError("No word / dictionary file was found.") from e
    except PermissionError as e:
        raise PermissionError("Access to dictionary file was denied.") from e
    return words

def get_input() -> str:
    '''
    This function asks the user to input the word they chose.

    Returns:
        word [str]: Holds the word that the user inputted.
        
    Raises:
        ValueError: User failed to input a valid word in the given 5 attempts.
    ''' 
    
    MAX_ATTEMPTS = 5
    for _ in range(MAX_ATTEMPTS):
        word = input("Word: ").strip().lower()

        if not word:
            print("Empty input. Try again.")
            continue

        if len(word) != 5:
            print("Word must be 5 letters.")
            continue

        if not word.isascii():
            print("Only standard English letters allowed.")
            continue

        if not word.isalpha():
            print("No numbers or punctuation.")
            continue
        
        return word
    raise ValueError("Too many invalid attempts.")
        
def get_colours(overall_green: List[str] = None, overall_yellow: List[str] = None, overall_grey: List[str] = None) -> List[str]:
    '''

    This function is used to both keep track of the overall information of the game, as well as
    create and fill the overall colour lists.
    
    Args:
        overall_green List[str] (default: None): A list of all the green letters
        overall_grey List[str] (default: None): A list of all the grey letters
        overall_yellow List[str] (default: None): A list of all the yellow letters

    Returns:
        letters List[char]: A list of the given colour type.
    '''
    
    if overall_green is None:
        overall_green = []
    if overall_yellow is None:
        overall_yellow = []
    if overall_grey is None:
        overall_grey = []

    choice = get_input()

    greens = get_feedback_letters("greens", choice)
    yellows = get_feedback_letters("yellow", choice)
    greys = list(choice)
    
    for letter in greens + yellows:
        if letter in greys:
            greys.remove(letter)
        
    if overall_green is not None:
        overall_green.extend(greens)
        overall_yellow.extend(yellows)
        overall_grey.extend(greys)
    
    return overall_green, overall_yellow, overall_grey, choice
    
def get_feedback_letters(colour_name: str, choice: str) -> List[str]:
    '''
    This function is used in get_colours() to find out what letters of the user's word were
    what colours.
    
    Args:
        colour_name [str]: The colour name (green, yellow or grey).
        choice [str]: The user's chosen word. 
    
    Returns:
        letters List[char]: A list of the given colour type. 
    '''
    letters = []
    while True:
            letters = input(f"What letters were {colour_name}? Enter none if no letters of that type were found: ").strip().lower()
            if letters == "none":
                return []
            elif any(char not in choice for char in list(letters)):
                print(f"A letter was not found in {choice}. Try again.")
            else:
                break
    return list(letters)

def compile_colours(green: List[str], grey: List[str], yellow: List[str], choice: str) -> List[str]:
    '''
    This function compiles a list (not a literal list) of the 3 colour types, which will be 
    used later as criteria for fidning valid words.
    
    Args:
        green List[str]: A list of the green letters
        grey List[str]: A list of the grey letters
        yellow List[str]: A list of the yellow letters
        choice [str]: The user's inputted word
    
    Returns:
        green_letters List[str]: A list of the green letters
        grey_letters List[str]: A list of the grey letters
        yellow_letters List[str]: A list of the yellow letters
    '''

    green_letters = {}
    yellow_letters = {}
    grey_letters = []
    
    for pos, char in enumerate(choice): 
        if char in green:
            green_letters[pos] = char  

        if char in yellow:
            yellow_letters.setdefault(char, []).append(pos) 

        if char in grey and char not in green and char not in yellow:
            grey_letters.append(char)
            
    return green_letters, yellow_letters, grey_letters
            
def find_words(green: List[str], yellow: List[str], grey: List[str], valid_words_list: List[str]) -> List[str]:
    '''
    This function finds all words that could possibly be the answer to the Wordle. 
    
    Args:
        green List[str]: A list of the green letters
        grey List[str]: A list of the grey letters
        yellow List[str]: A list of the yellow letters
    '''
    
    valid = []

    for word in valid_words_list:

        if any(letter in word for letter in grey):
            continue

        if any(word[pos] != letter for pos, letter in green.items()):
            continue

        bad_yellow = False
        for letter, positions in yellow.items():

            if letter not in word:
                bad_yellow = True
                break

            if any(word[pos] == letter for pos in positions):
                bad_yellow = True
                break

        if bad_yellow:
            continue

        valid.append(word)

    return valid

def print_valid(valid_words: List[str]) -> None:
    for w in valid_words:
        print(w)
    print(f"{len(valid_words)} possible words:")
def continue_program(overall_green: List[str], overall_yellow: List[str], overall_grey: List[str], valid_words: List[str]) -> None:
    '''
    This function acts as the looping logic. It allows the user to continue passing words in,
    such that they can narrow down the answer. 
    
    Raises:
        ValueError: User failed to input a valid word in the given 5 attempts.
        
    Args:
        overall_green List[str]: a list of all the green letters
        overall_grey List[str]: a list of all the grey letters
        overall_yellow List[str]: a list of all the yellow letters
    '''
    
    MAX_ATTEMPTS = 5
    for _ in range(MAX_ATTEMPTS):
        word = input("Are you finished? ").strip().lower()

        if not word:
            print("Empty input. Try again.")
            continue

        if not word.isascii():
            print("Only standard English letters allowed.")
            continue

        if not word.isalpha():
            print("No numbers or punctuation.")
            continue

        if word in ["y", "yes"]:
            exit(1)
        else:
            overall_green, overall_yellow, overall_grey = [], [], []
            
            overall_green, overall_yellow, overall_grey, choice = get_colours(overall_green, overall_yellow, overall_grey)
            green_letters, yellow_letters, grey_letters = compile_colours(overall_green, overall_grey, overall_yellow, choice)
            valid_words = find_words(green_letters, yellow_letters, grey_letters, valid_words)
            
            print_valid(valid_words)
    raise ValueError("Too many invalid attempts.")

def main():
    overall_green = []
    overall_yellow = []
    overall_grey = []
    
    valid_words = get_words()
    
    overall_green, overall_yellow, overall_grey, choice = get_colours(overall_green, overall_yellow, overall_grey)
    green_letters, yellow_letters, grey_letters = compile_colours(overall_green, overall_grey, overall_yellow, choice)
    
    valid_words = find_words(green_letters, yellow_letters, grey_letters, valid_words)
    print_valid(valid_words)
    
    continue_program(overall_green, overall_yellow, overall_grey, valid_words)
    
if __name__ == "__main__":
    main()