def get_words():
    '''
    This function looks at words.txt, a text file containing hundreds of thousands of words
    and then puts any 5 letter, english words that have no numbers into a list and returns it.
    
    
    Returns:
        words List[str]: contains a list of every valid word.
    
    Raisse:
        FileNotFoundError: no valid word or dictionary of words list was found.
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
    return words

def get_input():
    '''
    This function asks the user to input the word they chose.
    
    Returns:
        word [str]: holds the word that the user inputted.
        
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
        
def get_colours():
    '''
    This function asks the user to input how many of each letter type they got, then asks 
    (using another function) which letter(s) were what colour.
    '''

    choice = get_input()
    green, yellow, grey = [], [], []
    
    yellows_count = int(input("How many yellow characters did you get? Enter 0 if none: "))
    greens_count = int(input("How many green characters did you get? Enter 0 if none: "))
    greys_count = int(input("How many grey characters did you get? Enter 0 if none: "))
    
    yellows = get_feedback_letters("yellow", yellows_count, choice)
    greens = get_feedback_letters("green", greens_count, choice)
    greys = get_feedback_letters("grey", greys_count, choice)
    
    green = greens
    yellow = yellows
    grey = greys
    
    compile_colours(green, grey, yellow, choice)
    
def get_feedback_letters(color_name: str, count: int, choice: str):
    '''
    This function is used in get_colours() to find out what letters of the user's word were
    what colours.
    
    Args:
        colour_name [str]: the colour name (green, yellow or grey).
        count [int]: the amount of the given colour, which is then used for the loop count.
        choice [str]: the user's chosen word. 
    
    Returns:
        letters List[char]: a list of the given colour type. 
    '''
    
    letters = []
    for _ in range(count):
        while True:
            letter = input(f"What letter was {color_name}?: ").strip().lower()
            if letter in choice:
                letters.append(letter)
                break
            print(f"{letter} is not in {choice}. Try again.")
            
    return letters

def compile_colours(green, grey, yellow, choice):
    '''
    This function compiles a list (not a literal list) of the 3 colour types, which will be 
    used later as criteria for fidning valid words.
    
    Args:
        green List[str]: a list of the green letters
        grey List[str]: a list of the grey letters
        yellow List[str]: a list of the yellow letters
    '''

    green_letters = {}
    yellow_letters = {}
    grey_letters = set()
    
    for pos, char in enumerate(choice): 
        if char in green:
            green_letters[pos] = char  

        if char in yellow:
            yellow_letters.setdefault(char, []).append(pos) 

        if char in grey:
            grey_letters.add(char)
            
    find_words(green_letters, yellow_letters, grey_letters)
            
def find_words(green, yellow, grey):
    '''
    This function finds all words that could possibly be the answer to the Wordle. 
    
    Args:
        green List[str]: a list of the green letters
        grey List[str]: a list of the grey letters
        yellow List[str]: a list of the yellow letters
    '''
    
    words = get_words()
    valid = []

    for word in words:

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

    print_valid(valid)

def print_valid(valid_words):
    '''
    This function prints out every valid word.
    
    Args:
        valid_words List[str]: a list of every possible answer.
    '''

    print("Possible words:")
    for w in valid_words:
        print(w)
    continue_program()

def continue_program():
    '''
    This function acts as the looping logic. It allosw the user to continue passing words in,
    such that they can narrow down the answer. 
    
    Raises:
        ValueError: User failed to input a valid word in the given 5 attempts.
    
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
            get_colours()
    raise ValueError("Too many invalid attempts.")

def main():
    
    get_colours()
    
main()