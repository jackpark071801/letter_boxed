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

def find_words_for_all_starting_letters(words, letter_square):
    all_valid_words = {}
    used_letters_per_word = {}
    
    for side in letter_square:
        for start_letter in side:
            valid_words = [word for word in words if word[0] == start_letter and is_valid_word(word, letter_square)]
            if valid_words:
                all_valid_words[start_letter] = valid_words
                
                for word in valid_words:
                    used_letters_per_word[word] = set(word)
    
    return all_valid_words, used_letters_per_word

def suggest_best_starting_words(all_valid_words, used_letters_per_word, letter_square):
    word_scores = []
    
    square_letters = {letter for side in letter_square for letter in side}
    
    for start_letter, words in all_valid_words.items():
        for word in words:
            letters_used_from_square = used_letters_per_word[word].intersection(square_letters)
            word_scores.append((word, len(letters_used_from_square)))
    
    word_scores.sort(key=lambda x: x[1], reverse=True)
    
    best_words = [word for word, score in word_scores if score == word_scores[0][1]]
    
    return best_words, word_scores

def find_next_word(current_word, all_valid_words, used_letters, letter_square):
    last_letter = current_word[-1]
    
    if last_letter in all_valid_words:
        possible_words = all_valid_words[last_letter]
    else:
        return None
    
    best_next_word = None
    max_new_letters = 0
    
    for word in possible_words:
        new_letters = set(word) - used_letters
        if len(new_letters) > max_new_letters:
            best_next_word = word
            max_new_letters = len(new_letters)
    
    return best_next_word

def find_solution(letter_square, words):
    all_valid_words, used_letters_per_word = find_words_for_all_starting_letters(words, letter_square)
    
    best_words, _ = suggest_best_starting_words(all_valid_words, used_letters_per_word, letter_square)
    
    current_word = best_words[0]
    used_letters = set(current_word)
    solution = [current_word]
    
    while len(used_letters) < 16:
        next_word = find_next_word(current_word, all_valid_words, used_letters, letter_square)
        if not next_word:
            break
        
        solution.append(next_word)
        used_letters.update(set(next_word))
        current_word = next_word
    
    return solution

def main():
    json_file = 'english_words.json'
    
    words = load_words(json_file)

    letter_square = [
        ['N', 'E', 'P'],
        ['A', 'H', 'G'],
        ['R', 'I', 'K'],
        ['C', 'O', 'L']
    ]

    solution = find_solution(letter_square, words)

    print(solution)

if __name__ == "__main__":
    main()
