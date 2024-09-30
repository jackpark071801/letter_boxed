import json

def load_words(json_file):
    with open(json_file, 'r') as file:
        words = json.load(file)
    return words

def is_on_side(letter, side):
    return letter in side

def find_side(letter, letter_square):
    for i, side in enumerate(letter_square):
        if is_on_side(letter, side):
            return i
    return None

def is_valid_word(word, letter_square):
    prev_side = find_side(word[0], letter_square)
    
    if prev_side is None:
        return False

    for letter in word[1:]:
        current_side = find_side(letter, letter_square)
        if current_side is None or current_side == prev_side:
            return False
        prev_side = current_side
    
    return True

def filter_words_by_square(words, letter_square, start_letter):
    valid_words = [word for word in words if word[0] == start_letter]
    
    valid_words = [word for word in valid_words if is_valid_word(word, letter_square)]
    
    return valid_words

def main():
    json_file = 'english_words.json'
    
    words = load_words(json_file)

    letter_square = [
        ['A', 'B', 'C', 'D'],
        ['E', 'F', 'G', 'H'],
        ['I', 'J', 'K', 'L'],
        ['M', 'N', 'O', 'P']
    ]

    start_letter = 'A'

    valid_words = filter_words_by_square(words, letter_square, start_letter)

    print(valid_words[:20])

if __name__ == "__main__":
    main()
