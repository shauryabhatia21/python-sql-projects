# STRING PROCESSING ALGORITHMS
# Covers: Palindromes (loop & slice), case conversions, vowel/consonant character classification

def check_palindrome_loop(text):
    rev = ""
    for ch in text:
        rev = ch + rev
    is_pal = (rev.lower() == text.lower())
    print(f"Loop Palindrome Check for '{text}': {'PALINDROME' if is_pal else 'NOT PALINDROME'}")
    return is_pal

def check_palindrome_slice(text):
    is_pal = (text.lower() == text[::-1].lower())
    print(f"Slice Palindrome Check for '{text}': {'PALINDROME' if is_pal else 'NOT PALINDROME'}")
    return is_pal

def swap_case_string(text):
    result = text.swapcase()
    print(f"Case Inversion: '{text}' -> '{result}'")
    return result

def classify_characters(text):
    alphabets = 0
    digits = 0
    vowels = 0
    consonants = 0
    vowel_chars = "aeiouAEIOU"

    for ch in text:
        if ch.isalpha():
            alphabets += 1
            if ch in vowel_chars:
                vowels += 1
            else:
                consonants += 1
        elif ch.isdigit():
            digits += 1

    print(f"Analysis for '{text}':")
    print(f"  - Total Alphabets : {alphabets}")
    print(f"  - Vowels          : {vowels}")
    print(f"  - Consonants      : {consonants}")
    print(f"  - Digits          : {digits}")

if __name__ == '__main__':
    print("--- 1. Palindrome Tests ---")
    check_palindrome_loop("madam")
    check_palindrome_loop("python")
    check_palindrome_slice("racecar")

    print("\n--- 2. Case Conversion ---")
    swap_case_string("Hello World 123!")

    print("\n--- 3. Character Classification ---")
    classify_characters("ShauryaBhatia10@Python2026")
