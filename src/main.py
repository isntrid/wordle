

def get_files():
    words = set()
    with open("words.txt", 'r') as w:
        lines = w.readlines()
        for word in lines:
            words.add(word.strip())
    return words

print(get_files())