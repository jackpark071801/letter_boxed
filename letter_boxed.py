import json
from typing import List, Dict, Tuple, Optional

def load_words(
    json_file: str,
    ) -> List[str]:
    with open(json_file, 'r') as file:
        words = json.load(file)
    return words

def is_on_side(
    letter: str,
    side: int,
    ) -> bool:
    return letter in side

def find_side(
    letter: str,
    letter_square: List[List[str]],
    ) -> Optional[bool]:
    for i, side in enumerate(letter_square):
        if is_on_side(letter, side):
            return i
    return None

def is_valid_word(
    word: str,
    letter_square: List[List[str]],
    ) -> bool:
    prev_side = find_side(word[0], letter_square)
    
    if prev_side is None:
        return False

    for letter in word[1:]:
        current_side = find_side(letter, letter_square)
        if current_side is None or current_side == prev_side:
            return False
        prev_side = current_side
    
    return True

def filter_words_by_square(
    words: List[str],
    letter_square: List[List[str]],
    start_letter: str,
    ) -> List[str]:
    valid_words = [word for word in words if word[0] == start_letter]
    
    valid_words = [word for word in valid_words if is_valid_word(word, letter_square)]
    
    return valid_words

def find_words_for_all_starting_letters(
    words: List[str],
    letter_square: List[List[str]],
    ) -> Tuple[List[str], List[int]]:
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

def suggest_best_starting_words(
    all_valid_words: List[str],
    used_letters_per_word: Dict[str, int],
    letter_square: List[List[str]],
    ) -> Tuple[List[str], Dict[str, int]]:
    word_scores = []
    
    square_letters = {letter for side in letter_square for letter in side}
    
    for start_letter, words in all_valid_words.items():
        for word in words:
            letters_used_from_square = used_letters_per_word[word].intersection(square_letters)
            word_scores.append((word, len(letters_used_from_square)))
    
    word_scores.sort(key=lambda x: x[1], reverse=True)
    
    best_words = [word for word, score in word_scores if score == word_scores[0][1]]
    
    return best_words, word_scores

def find_next_word(
    current_word: str,
    all_valid_words: List[str],
    used_letters: List[str],
    letter_square: List[List[str]],
    ) -> Optional[str]:
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

def find_solution(
    letter_square: List[List[str]],
    words: List[str],
    ) -> List[str]:
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

def remove_word_from_json(
    word_to_remove: str,
    json_file_path: str,
    ) -> None:
    try:
        with open(json_file_path, 'r') as f:
            word_list = json.load(f)
        
        if word_to_remove.upper() in word_list:
            word_list.remove(word_to_remove.upper())
            print(f"Word '{word_to_remove}' removed from the list.")
        else:
            print(f"Word '{word_to_remove}' not found in the list.")
        
        with open(json_file_path, 'w') as f:
            json.dump(word_list, f)
            print(f"Updated word list saved to '{json_file_path}'.")
    
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{json_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    json_file = 'english_words.json'

    #remove_word_from_json('DANORANJA', json_file)
    
    words = load_words(json_file)

    letter_square = [
        ['H', 'D', 'P'],
        ['F', 'A', 'O'],
        ['N', 'S', 'C'],
        ['R', 'I', 'J']
    ]

    solution = find_solution(letter_square, words)

    print(solution)

if __name__ == "__main__":
    main()
