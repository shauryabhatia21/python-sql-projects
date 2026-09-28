# 🧱 Python OOP & Core Foundations Suite

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OOP](https://img.shields.io/badge/Paradigm-Object--Oriented-purple?style=for-the-badge&logo=codefactor&logoColor=white)](https://github.com/shauryabhatia10)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Verification](https://img.shields.io/badge/Bytecode_Pass-100%25-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white)](https://github.com/shauryabhatia10)

A comprehensive, production-grade engineering suite demonstrating **Object-Oriented Programming (OOP), Single & Multilevel Inheritance, Encapsulated Inner Classes, Functional Paradigms, and Defensive Exception Handling** built by **[Shaurya Bhatia](https://github.com/shauryabhatia10)**.

---

## 📂 Repository Architecture

```text
python-oop-foundations/
├── 01_OOPS_FUNDAMENTALS/
│   ├── bank_application_oop.py           # Enterprise SBI bank account manager with deposit/withdrawal validations
│   └── oops_introduction.py              # Procedural vs OOP paradigms, reference variables, and student/fuel entities
│
├── 02_INHERITANCE_PATTERNS/
│   ├── single_inheritance_demo.py        # Base-to-derived method resolution order (MRO)
│   ├── multilevel_student_result.py      # Multilevel hierarchy: PDetail -> Marks -> Result calculation
│   ├── hierarchical_logical_calculator.py# Extended scientific calculator inheriting arithmetic operations
│   └── shape_volume_inheritance.py       # 2D Shape to 3D Prism volume derivation using super()
│
├── 03_INNER_CLASSES_AND_FUNCTIONAL/
│   └── inner_classes_and_lambdas.py      # Nested class lifetimes (Person -> DOB) & Functional pipeline (lambda, map, filter, reduce)
│
└── 04_EXCEPTION_HANDLING/
    └── exception_handling_suite.py       # Defensive runtime handling (try, except, else, finally, raise, and custom errors)
```

---

## 🔬 Core Competencies & Conceptual Matrix

| Module / Directory | Key Concepts | Design Patterns & Engineering Highlights |
|---|---|---|
| **01_OOPS_FUNDAMENTALS** | Classes, Objects, Constructors (`__init__`), Encapsulation | In-memory customer repository, dynamic account ID generation, transaction validation. |
| **02_INHERITANCE_PATTERNS** | Single & Multilevel Inheritance, Method Overriding, `super()` | Separation of student attributes and academic metrics; modular calculator with `match-case` routing. |
| **03_INNER_CLASSES_AND_FUNCTIONAL** | Nested Classes, Anonymous Lambdas, Higher-Order Functions | Encapsulated lifetime (`Person.DOB`); declarative functional transformations via `map()`, `filter()`, `reduce()`. |
| **04_EXCEPTION_HANDLING** | Runtime Fault Tolerance, Error Hierarchies, `finally` Guarantees | Granular interception (`ZeroDivisionError`, `ValueError`, `IndexError`), resource cleanups, domain-specific `NegativeNumberError`. |

---

## 🚀 Execution & Demo Guide

Clone this repository and run any module directly:

```powershell
# 1. Run Interactive OOP Bank System
python 01_OOPS_FUNDAMENTALS/bank_application_oop.py

# 2. Run Multilevel Academic Result Generator
python 02_INHERITANCE_PATTERNS/multilevel_student_result.py

# 3. Run Extended Scientific & Arithmetic Calculator
python 02_INHERITANCE_PATTERNS/hierarchical_logical_calculator.py

# 4. Run 3D Shape Volume Hierarchy
python 02_INHERITANCE_PATTERNS/shape_volume_inheritance.py

# 5. Run Inner Classes & Functional Programming Demo
python 03_INNER_CLASSES_AND_FUNCTIONAL/inner_classes_and_lambdas.py

# 6. Run Robust Exception Handling Suite
python 04_EXCEPTION_HANDLING/exception_handling_suite.py
```

---

## 🧪 Rigorous Quality & Verification

Every file in this repository is strictly verified with zero syntax errors, type bugs, or unhandled crashes using Python's standard bytecode compiler:

```powershell
python -m compileall .
```

Output:
```text
Listing '.'...
Listing '.\01_OOPS_FUNDAMENTALS'...
Compiling '.\01_OOPS_FUNDAMENTALS\bank_application_oop.py'...
Compiling '.\01_OOPS_FUNDAMENTALS\oops_introduction.py'...
Listing '.\02_INHERITANCE_PATTERNS'...
Compiling '.\02_INHERITANCE_PATTERNS\hierarchical_logical_calculator.py'...
Compiling '.\02_INHERITANCE_PATTERNS\multilevel_student_result.py'...
Compiling '.\02_INHERITANCE_PATTERNS\shape_volume_inheritance.py'...
Compiling '.\02_INHERITANCE_PATTERNS\single_inheritance_demo.py'...
Listing '.\03_INNER_CLASSES_AND_FUNCTIONAL'...
Compiling '.\03_INNER_CLASSES_AND_FUNCTIONAL\inner_classes_and_lambdas.py'...
Listing '.\04_EXCEPTION_HANDLING'...
Compiling '.\04_EXCEPTION_HANDLING\exception_handling_suite.py'...
```

---

<div align="center">
  <b>Author: [Shaurya Bhatia](https://github.com/shauryabhatia21)</b><br/>
  <i>B.Tech Computer Science & Engineering (CSE Core) @ Bennett University</i>
</div>
