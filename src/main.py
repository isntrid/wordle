

def get_files():
    with open("words.txt", 'r') as w:
        
        lines = w.readlines()
        words = [
            word for w in lines 
            if (word := w.strip().lower()).isalpha() 
            and word.isascii() and len(word) == 5
            ]
        
    return words

