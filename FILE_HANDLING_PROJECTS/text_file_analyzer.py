# TEXT FILE ANALYZER & UTILITY
# Demonstrates reading, writing, counting occurrences of specific words, replacing words, and counting vowels

import os

def create_sample_file(filename="sample.txt"):
    content = "The quick brown fox jumps over the lazy dog.\nThe sun shines bright in the morning sky.\n"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sample file '{filename}' created.")

def count_word(filename="sample.txt", target="the"):
    count = 0
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return 0
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            words = line.lower().split()
            count += words.count(target.lower())
    print(f"Total occurrences of word '{target}' in '{filename}': {count}")
    return count

def count_vowels(filename="sample.txt"):
    vowels = "aeiouAEIOU"
    vowel_count = 0
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return 0
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            for ch in line:
                if ch in vowels:
                    vowel_count += 1
    print(f"Total vowels in '{filename}': {vowel_count}")
    return vowel_count

def replace_word(filename="sample.txt", old_word="the", new_word="that"):
    if not os.path.exists(filename):
        return
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace(old_word, new_word).replace(old_word.capitalize(), new_word.capitalize())
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Replaced '{old_word}' with '{new_word}' in '{filename}'.")

if __name__ == '__main__':
    create_sample_file()
    count_word("sample.txt", "the")
    count_vowels("sample.txt")
    replace_word("sample.txt", "the", "that")
