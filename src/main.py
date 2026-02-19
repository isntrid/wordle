

def get_files():
    
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
        
def check(word):
    
    grey, green, yellow = [], [], []
    