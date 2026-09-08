import pandas as pd
import random
from datetime import date, timedelta

def genIssueId():
    return "ISS" + str(random.randint(100, 999))

def issueBook():
    # Read books file:
    try:
        books_df = pd.read_csv("books.csv")
    except Exception:
        print("books.csv not found! Please add books first.")
        return

    # Create issue.csv if it does not exist:
    try:
        issue_df = pd.read_csv("issue.csv")
    except Exception:
        issue_df = pd.DataFrame(columns=["Issue_ID", "BOOK_ID", "MEM_ID", "ISSUE_DATE", "DUE_DATE"])
        issue_df.to_csv("issue.csv", index=False)

    # INPUT
    bid = input("Enter book ID: ")
    mid = input("Enter mem ID: ")

    # CHECK WHETHER BOOK EXISTS:
    if bid not in books_df["BOOK_ID"].values:
        print('Book does not exist')
        return

    # Check book availability:
    status = books_df.loc[books_df['BOOK_ID'] == bid, 'STATUS'].values[0]
    if status == "NO":
        print("Book is already issued.")
        return

    # GENERATE Issue id and dates:
    issue_id = genIssueId()
    issue_date = date.today()
    due_date = issue_date + timedelta(days=10)

    # Update status of book to NO:
    books_df.loc[books_df['BOOK_ID'] == bid, 'STATUS'] = "NO"
    books_df.to_csv("books.csv", index=False)

    # Add issue record:
    issue_df = pd.read_csv("issue.csv")
    issue_df.loc[len(issue_df)] = [issue_id, bid, mid, issue_date, due_date]
    issue_df.to_csv("issue.csv", index=False)

    print("BOOK ISSUED Successfully")
    print("ISSUE ID:", issue_id)
    print("ISSUE DATE:", issue_date)
    print("DUE DATE:", due_date)

def returnBook():
    try:
        books_df = pd.read_csv("books.csv")
        issue_df = pd.read_csv("issue.csv")
    except Exception:
        print("Required CSV files not found.")
        return

    iss_id = input("Enter Issue ID to return: ")
    if iss_id not in issue_df["Issue_ID"].values:
        print("Issue ID not found.")
        return

    bid = issue_df.loc[issue_df["Issue_ID"] == iss_id, "BOOK_ID"].values[0]
    # Update book status back to YES:
    books_df.loc[books_df["BOOK_ID"] == bid, "STATUS"] = "YES"
    books_df.to_csv("books.csv", index=False)

    # Remove issue record:
    issue_df = issue_df.loc[issue_df["Issue_ID"] != iss_id]
    issue_df.to_csv("issue.csv", index=False)
    print(f"Book {bid} returned successfully!")

def transactionMenu():
    while True:
        print("--- ISSUE / RETURN MENU ---")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. View Issued Books")
        print("4. Return to Main Menu")
        try:
            ch = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue

        if ch == 1:
            issueBook()
        elif ch == 2:
            returnBook()
        elif ch == 3:
            try:
                issue_df = pd.read_csv("issue.csv")
                print(issue_df.to_string(index=False))
            except Exception:
                print("No issued books recorded.")
        elif ch == 4:
            return
        else:
            print("Invalid Choice")
