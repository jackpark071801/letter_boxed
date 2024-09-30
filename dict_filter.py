import json

def load_words(json_file):
    with open(json_file, 'r') as file:
        words = json.load(file)
    return words

def filter_words(words):
    return [word.upper() for word in words if len(word) > 4]

def save_filtered_words(filtered_words, output_file):
    with open(output_file, 'w') as file:
        json.dump(filtered_words, file, indent=4)
    print(f"Filtered words saved to {output_file}")

def main():
    json_file = 'words_dictionary.json'
    
    output_file = 'D:/Fun_Programs/Letter Boxed/english_words.json'
    
    words = load_words(json_file)
    
    filtered_words = filter_words(words)
    
    save_filtered_words(filtered_words, output_file)

if __name__ == "__main__":
    main()