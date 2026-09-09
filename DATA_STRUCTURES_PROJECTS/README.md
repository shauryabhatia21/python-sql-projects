# 📊 Python Data Structures & Collections (Lists, Dictionaries & Tuples)

A comprehensive suite of foundational and enterprise-level in-memory data structures demonstrating **Lists (dynamic arrays), Dictionaries (hash maps), and Tuples (immutable sequences)** built by **[Shaurya Bhatia](https://github.com/shauryabhatia10)**.

---

## 📂 Modules & Implementations

```text
DATA_STRUCTURES_PROJECTS/
├── list_operations_menu.py       # Interactive CLI menu for list manipulation (append, insert, pop, clear)
├── student_records_list.py       # Student roster management using nested list structures
├── student_records_dict.py       # Student database using dictionary key mapping to attribute lists
├── dictionary_foundations.py     # In-depth dictionary mechanics: keys(), values(), items(), safe lookups
├── tuple_foundations.py          # Immutable sequence architecture, built-in stats, packing & unpacking
├── bank_dict_system.py           # Core banking system using hash map lookups and P2P transfers
├── student_dict_system.py        # Academic CRUD record manager indexed by enrollment number
├── contact_book_dict.py          # Phone and address book with custom masked alphanumeric IDs
├── generators.py                 # Randomized unique account number and contact ID generator utilities
└── Classroom Foundations:
    ├── dictonary intro(COM).py       # Classroom notes & demonstrations for dictionaries
    ├── tupl intro(COM).py            # Classroom notes & demonstrations for tuples
    ├── dictonary(bank main menu)(COM).py
    ├── dictonary (student main menu)(COM).py
    ├── dictonary (contact list ).py
    └── List nested loop main menu(COM).py
```

---

## 🔬 Algorithmic & Structural Highlights

| Data Structure | Module | Time Complexity (Lookup / Access) | Key Operations Demonstrated |
|---|---|:---:|---|
| **List (Dynamic Array)** | `list_operations_menu.py` | $O(1)$ by index / $O(N)$ by value | `append()`, `insert(pos, val)`, `pop(0)`, `clear()`, index searching |
| **Nested Lists** | `student_records_list.py` | $O(N)$ traversal | 2D matrix-like student records `[eno, name, course, fee]`, fee accumulation |
| **Dictionary (Hash Map)** | `dictionary_foundations.py` | $O(1)$ average | Key uniqueness, `.keys()`, `.values()`, `.items()`, `.get()` safe fallback |
| **Dictionary + List** | `student_records_dict.py` | $O(1)$ by enrollment no | Primary key mapping to attribute lists, collision handling |
| **Tuple (Immutable)** | `tuple_foundations.py` | $O(1)$ index access | Single-element commas `(11,)`, `max()`, `min()`, `sum()`, tuple packing & unpacking |
| **Enterprise Hash Map** | `bank_dict_system.py` | $O(1)$ average | Account generation, balance deposits, overdraft validations, fund transfers |

---

## 🚀 How to Run

Navigate to this directory and run any module directly:

```powershell
# Run the Interactive List Operations Menu
python list_operations_menu.py

# Run the Dictionary Foundations Demo
python dictionary_foundations.py

# Run the Tuple Foundations Demo
python tuple_foundations.py

# Run the Student Nested Lists Manager
python student_records_list.py

# Run the Student Dictionary Manager
python student_records_dict.py

# Run the In-Memory Banking System
python bank_dict_system.py
```

---

## 🧪 Verification

All modules have been verified with 0 syntax or runtime errors using Python's bytecode compiler:
```powershell
python -m compileall .
```

---

<div align="center">
  <b>Author: [Shaurya Bhatia](https://github.com/shauryabhatia10)</b><br/>
  <i>Undergraduate in Artificial Intelligence @ Bennett University</i>
</div>
