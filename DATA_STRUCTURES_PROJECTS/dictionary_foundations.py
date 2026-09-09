# ==============================================================================
# Program: Dictionary Foundations & Methods Demonstration
# Author: Shaurya Bhatia (Bennett University)
# Description: Explores key-value pair architecture, uniqueness of keys,
#              in-place value mutation, keys/values/items traversals, and safe lookups.
# ==============================================================================

def demonstrate_dictionary_basics():
    print("=" * 60)
    print("        PYTHON DICTIONARY FOUNDATIONS & OPERATIONS")
    print("=" * 60)

    # 1. Blank dictionary generation
    blank_dict = {}
    print(f"1. Empty dictionary created: {blank_dict}, Type: {type(blank_dict)}")

    # 2. Initializing with sample records (Roll No -> Student Name)
    d1 = {1: "Aarav", 2: "Mahima", 3: "Rohan", 4: "Ishita"}
    print(f"\n2. Initialized Dictionary: {d1}")
    print(f"   Total entries: {len(d1)}")

    # 3. Accessing keys and values
    print("\n3. Dictionary Keys & Values:")
    print(f"   Keys List   : {list(d1.keys())}")
    print(f"   Values List : {list(d1.values())}")

    # 4. Iterating over keys
    print("\n4. Iterating using d1.keys():")
    for roll in d1.keys():
        print(f"   Roll No: {roll}  |  Student Name: {d1[roll]}")

    # 5. Iterating using d1.items() (Unpacking key-value pairs)
    print("\n5. Iterating using d1.items() (Tuple Unpacking):")
    for roll, name in d1.items():
        print(f"   Roll No: {roll:02d} -> {name}")

    # 6. Modifying an existing key vs inserting a new key
    print("\n6. Mutation Demonstration:")
    print(f"   Before modification: d1[2] = '{d1[2]}'")
    d1[2] = "Mahima Sharma"  # Key exists -> mutates existing value
    print(f"   After modification : d1[2] = '{d1[2]}'")

    d1[22] = "Rajeev"  # Key does not exist -> adds new key-value pair
    print(f"   After adding new key (22): {d1}")

    # 7. Safe lookup using get()
    print("\n7. Safe Lookups using .get():")
    search_key = 99
    print(f"   Looking for key {search_key}: {d1.get(search_key, 'Key Not Found (Safe Default)')}")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_dictionary_basics()
