# 📁 File Handling Systems in Python

Persistent disk data management utilizing binary serialization (`pickle`), comma-separated values (`csv`), and text files.

---

## 📂 Projects Index

1. **`bank_pickle_system.py`**:
   - Binary data storage in `customer.dat` via `pickle.dump()` and `pickle.load()`.
   - Safely updates disk records using temporary file swaps (`temp.dat` -> `customer.dat`).
   - Deposit, withdrawal, search, and customer record deletions.

2. **`student_csv_manager.py`**:
   - Tabular student database in `student_records.csv` using Python's native `csv` library.
   - Formatted column displays, append operations, and search.

3. **`text_file_analyzer.py`**:
   - File parsing algorithms: targeted word frequency counter, text replacement, and vowel detection.

---

## 🚀 How to Run

```powershell
python bank_pickle_system.py
python student_csv_manager.py
python text_file_analyzer.py
```
