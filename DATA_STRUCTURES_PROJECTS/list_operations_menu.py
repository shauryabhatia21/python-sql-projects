# ==============================================================================
# Program: List Operations Menu-Driven System
# Author: Shaurya Bhatia (Bennett University)
# Description: Demonstrates dynamic list manipulation, insertion, deletion,
#              search, and traversal using Python match-case construct.
# ==============================================================================

def list_menu():
    a1 = [11, 22, 33, 44, 55]

    while True:
        print("\n" + "=" * 50)
        print("          LIST OPERATIONS MENU")
        print("=" * 50)
        print(f"Current List: {a1}")
        print("1. Add element at the end (append)")
        print("2. Add element at specified position (insert)")
        print("3. Remove element from beginning (pop 0)")
        print("4. Display all elements")
        print("5. Search an element (by value)")
        print("6. Remove all elements (clear)")
        print("7. Exit")
        print("=" * 50)

        try:
            ch = int(input("Enter your choice (1-7): "))
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 7.")
            continue

        match ch:
            case 1:
                n = int(input("Enter element to append: "))
                a1.append(n)
                print(f"Successfully added! Updated list: {a1}")

            case 2:
                n = int(input("Enter element to insert: "))
                pos = int(input(f"Enter position index (0 to {len(a1)}): "))
                if 0 <= pos <= len(a1):
                    a1.insert(pos, n)
                    print(f"Successfully inserted! Updated list: {a1}")
                else:
                    print(f"Invalid position! Must be between 0 and {len(a1)}.")

            case 3:
                if len(a1) > 0:
                    removed = a1.pop(0)
                    print(f"Removed first element '{removed}'. Updated list: {a1}")
                else:
                    print("List is already empty! Nothing to remove.")

            case 4:
                print(f"All elements in list ({len(a1)} total):")
                for index, val in enumerate(a1):
                    print(f"  Index [{index}] -> {val}")

            case 5:
                n = int(input("Enter element to search: "))
                if n in a1:
                    idx = a1.index(n)
                    print(f"Element '{n}' found at index position {idx}!")
                else:
                    print(f"Element '{n}' not found in the list.")

            case 6:
                a1.clear()
                print(f"All elements removed! Updated list: {a1}")

            case 7:
                print("Exiting List Operations Menu. Goodbye!")
                break

            case _:
                print("Invalid choice! Please select an option between 1 and 7.")


if __name__ == "__main__":
    list_menu()
