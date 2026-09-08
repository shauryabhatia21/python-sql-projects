# Library Management System (Python + MySQL + Email Automation)

An automated Library Management System built with Python, MySQL, and SMTP Gmail integration.

## Features
- **Books Portal**: Add, search, update, delete, and view books with unique auto-generated Book IDs.
- **Members Portal**: Register members with auto-generated membership IDs, save joining date, and send automatic registration confirmation emails.
- **Issue & Return Portal**: Issue books with due date calculations, rental cost calculation, unique token generation, and return overdue fine management.
- **Automated Email Receipts**: Sends email confirmations to members via Gmail SMTP.

## Database Setup
1. Open MySQL Command Line Client or MySQL Workbench.
2. Run the `schema.sql` file:
   ```sql
   source schema.sql;
   ```

## Configuration
Update your database password in `db_config.py` (or set the `DB_PASSWORD` environment variable).
Update your email credentials in `email_config.py` (or set `SENDER_EMAIL` and `SENDER_PASSWORD` environment variables).

## Run the Project
```bash
python library_main_menu.py
```
