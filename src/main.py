

def get_words():
    
    with open("words.txt", 'r') as w:
        
        lines = w.readlines()
        words = [
            word for w in lines 
            if (word := w.strip().lower()).isalpha() 
            and word.isascii() and len(word) == 5
            ]
        
    return words

def get_input():
    
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
        
def get_yellows_greens():
    
    words = get_words()
    choice = get_input()
    green, yellow, grey = [], [], []
    
    yellows_count = int(input("How many yellow characters did you get? Enter 0 if none: "))
    greens_count = int(input("How many green characters did you get? Enter 0 if none: "))
    greys_count = int(input("How many grey characters did you get? Enter 0 if none: "))
    
    yellows = get_feedback_letters("yellow", yellows_count, choice)
    greens = get_feedback_letters("green", greens_count, choice)
    greys = get_feedback_letters("grey", greys_count, choice)
    
    green.append(greens)
    yellow.append(yellows)
    grey.append(greys)
    
    check_letters(green, grey, yellow)
    
def get_feedback_letters(color_name: str, count: int, choice: str):
    letters = []
    for _ in range(count):
        while True:
            letter = input(f"What letter was {color_name}?: ").strip().lower()
            if letter in choice:
                letters.append(letter)
                break
            print(f"{letter} is not in {choice}. Try again.")
            
    return letters

def check_letters(green, grey, yellow):
    pass