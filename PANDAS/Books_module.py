import random
import pandas as pd

def booksMenu():
    try:
        books_df=pd.read_csv('books.csv')
    except Exception as e:
        books={'BOOK_ID':['ITSB001','ITSB123','ITSB124'],
               'BOOK_NAME':['C','C++','PYTHON'],
               'PUBLISHER':['BPB','TATA','BPB'],
               'AUTHOR':['YESHWANT','GOSHLIN','JUDIO'],
               'STATUS':['YES','YES','YES']}
        books_df=pd.DataFrame(books)
        books_df.to_csv('books.csv',index=False)

    def genBid():
        a=random.randint(0,9)
        b=random.randint(0,9)
        c=random.randint(0,9)
        return 'ITSB'+str(a)+str(b)+str(c)

    while True:
        print('--- BOOK MENU ---')
        print('1. Add New Book')
        print('2. Remove Book')
        print('3. Search Book')
        print('4. Modify Existing Book')
        print('5. Display All book')
        print('6. Goto Main Menu')
        try:
            choice=int(input('Enter your choice: '))
        except ValueError:
            print('Please enter a valid number')
            continue

        if choice==1:
            b_id=genBid()
            bname=input('Enter book name: ')
            pub=input('Enter publisher: ')
            author=input('Enter author: ')
            status='YES'

            books_df=pd.read_csv('books.csv')
            books_df.loc[len(books_df)]=[b_id,bname,pub,author,status]
            books_df.to_csv('books.csv',index=False)
            print(f'Book added successfully with ID: {b_id}')
        elif choice==2:
            bid=input('Enter book id to remove: ')
            books_df=pd.read_csv('books.csv')
            books_df=books_df.loc[books_df['BOOK_ID']!=bid]
            books_df.to_csv('books.csv',index=False)
            print('Book removed if existed')
        elif choice==3:
            bid=input('Enter book id to search: ')
            books_df=pd.read_csv('books.csv')
            result=books_df.loc[books_df['BOOK_ID']==bid]
            if result.empty:
                print('book not found')
            else:
                print(result.to_string(index=False))
        elif choice==4:
            bid=input('Enter book id to modify : ')
            df=pd.read_csv('books.csv')
            if bid in df['BOOK_ID'].values:
                index=df[df['BOOK_ID']==bid].index
                print('Leave blank if no change required')
                bname=input('Enter New Book Name: ')
                pub=input('Enter New Publisher name: ')
                author=input('Enter New Author Name: ')
                status=input('Enter new status: ')

                if bname !='':
                    df.loc[index,'BOOK_NAME']=bname
                if pub !='':
                    df.loc[index,'PUBLISHER']=pub
                if author !='':
                    df.loc[index,'AUTHOR']=author
                if status !='':
                    df.loc[index,'STATUS']=status
                df.to_csv('books.csv', index=False)
                print('Book modified successfully')
            else:
                print('Book Id not found.')
        elif choice==5:
            books_df=pd.read_csv('books.csv')
            print(books_df.to_string(index=False))
        elif choice==6:
            return
        else:
            print('invalid choice')
