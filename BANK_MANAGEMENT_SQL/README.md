# Bank Management System (Python & MySQL)

A console-based Banking System for managing customer accounts in a MySQL database.

## Features
- **Add Customer**: Open accounts with Account Number, Customer Name, Account Type (Savings/Current), and Initial Balance.
- **Search Customer**: Query customer records by Account Number.
- **Change Account Type**: Update customer account type.
- **Display All Records**: Formatted list of all banking customers and balances.
- **Delete Customer**: Remove customer record from database.

## Database Setup
Run `schema.sql` in MySQL:
```sql
source schema.sql;
```

## Running
```bash
python bank_main_menu.py
```
