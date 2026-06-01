import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk


def connect_db():
    conn = mysql.connector.connect(
        host="localhost",        
        user="root",             
        password="root",         
    )
    cursor = conn.cursor()
    return conn, cursor


def setup_database():
    conn, cursor = connect_db()
    
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    cursor.execute("USE library_db")
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS BookDetails (
                        BookID INT AUTO_INCREMENT PRIMARY KEY,
                        Title VARCHAR(255) NOT NULL,
                        Author VARCHAR(255) NOT NULL,
                        PublishedYear INT NOT NULL
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS MemberDetails (
                        MemberID INT AUTO_INCREMENT PRIMARY KEY,
                        Name VARCHAR(255) NOT NULL,
                        PhoneNumber VARCHAR(15) NOT NULL,
                        BorrowDate DATE,
                        ReturnDate DATE,
                        BookID INT,
                        FOREIGN KEY (BookID) REFERENCES BookDetails(BookID)
                    )''')
    
    conn.commit()
    conn.close()


def save_book():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("INSERT INTO BookDetails (Title, Author, PublishedYear) VALUES (%s, %s, %s)", 
                   (title_var.get(), author_var.get(), year_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book details added successfully")
    read_book()  


def update_book():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("UPDATE BookDetails SET Title = %s, Author = %s, PublishedYear = %s WHERE BookID = %s",
                   (title_var.get(), author_var.get(), year_var.get(), book_id_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book details updated successfully")
    read_book()  

def delete_book():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("DELETE FROM BookDetails WHERE BookID = %s", (book_id_var.get(),))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book details deleted successfully")
    read_book()  


def save_member():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("INSERT INTO MemberDetails (Name, PhoneNumber, BorrowDate, ReturnDate, BookID) VALUES (%s, %s, %s, %s, %s)",
                   (name_var.get(), phone_var.get(), borrow_date_var.get(), return_date_var.get(), book_id_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Member details added successfully")
    read_member()  


def update_member():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("UPDATE MemberDetails SET Name = %s, PhoneNumber = %s, BorrowDate = %s, ReturnDate = %s, BookID = %s WHERE MemberID = %s",
                   (name_var.get(), phone_var.get(), borrow_date_var.get(), return_date_var.get(), book_id_var.get(), member_id_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Member details updated successfully")
    read_member()  


def delete_member():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("DELETE FROM MemberDetails WHERE MemberID = %s", (member_id_var.get(),))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Member details deleted successfully")
    read_member()  


def set_background(image_path):
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((800, 500), Image.Resampling.LANCZOS)  
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        
        bg_label = tk.Label(right_frame, image=bg_photo, bg="white")
        bg_label.image = bg_photo  
        bg_label.pack(expand=True, fill=tk.BOTH)
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Image file not found: {e}")


def read_book():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("SELECT * FROM BookDetails")
    rows = cursor.fetchall()
    conn.close()

    
    for widget in book_data_frame.winfo_children():
        widget.destroy()

    tk.Label(book_data_frame, text="Book Details", font=('Helvetica', 16, 'bold')).pack(pady=10)

    
    columns = ('BookID', 'Title', 'Author', 'Published Year')
    tree = ttk.Treeview(book_data_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    
    for row in rows:
        tree.insert('', 'end', values=row)

    tree.pack(pady=10, fill=tk.BOTH, expand=True)


def read_member():
    conn, cursor = connect_db()
    cursor.execute("USE library_db")
    cursor.execute("SELECT * FROM MemberDetails")
    rows = cursor.fetchall()
    conn.close()

    
    for widget in member_data_frame.winfo_children():
        widget.destroy()

    tk.Label(member_data_frame, text="Member Details", font=('Helvetica', 16, 'bold')).pack(pady=10)

    
    columns = ('MemberID', 'Name', 'PhoneNumber', 'Borrow Date', 'Return Date', 'BookID')
    tree = ttk.Treeview(member_data_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    
    for row in rows:
        tree.insert('', 'end', values=row)

    tree.pack(pady=10, fill=tk.BOTH, expand=True)


def welcome_page():
    clear_frame()
    set_background("image112.jpg")  

    tk.Label(top_frame, text="Welcome to the Library Management System", font=('Helvetica', 40, 'bold'), 
             bg="white", fg="darkblue").pack(pady=20, fill=tk.X)

    description = "Welcome to the Library Management System. Access book and member details with ease. Manage your library efficiently and effectively."
    tk.Label(left_frame, text=description, font=('Helvetica', 18), bg="white", fg="black", wraplength=350, justify="center").pack(pady=(200, 30))

    
    button_frame = tk.Frame(left_frame, bg="white")
    button_frame.pack(pady=20, expand=True, anchor='center')

    button_width = 20  
    tk.Button(button_frame, text="Go to Book Details", command=book_page, bg="orange", fg="white", font=('Helvetica', 18), width=button_width).pack(pady=10)
    tk.Button(button_frame, text="Go to Member Details", command=member_page, bg="orange", fg="white", font=('Helvetica', 18), width=button_width).pack(pady=10)


def book_page():
    clear_frame()
    set_background("image112.jpg")

    tk.Label(top_frame, text="Book Details", font=('Helvetica', 30, 'bold'), bg="darkblue", fg="white").pack(pady=10, fill=tk.X)

    global book_id_var, title_var, author_var, year_var
    book_id_var = tk.StringVar()
    title_var = tk.StringVar()
    author_var = tk.StringVar()
    year_var = tk.StringVar()

    
    form_frame = tk.Frame(left_frame, bg="white")
    form_frame.pack(pady=30, expand=True, anchor='center')

    create_labeled_entry("Book ID (For Update/Delete)", book_id_var, form_frame)
    create_labeled_entry("Title", title_var, form_frame)
    create_labeled_entry("Author", author_var, form_frame)
    create_labeled_entry("Published Year", year_var, form_frame)

    
    button_frame = tk.Frame(form_frame, bg="white")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Save", command=save_book, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Update", command=update_book, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete", command=delete_book, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Read", command=read_book, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)

    
    global book_data_frame
    book_data_frame = tk.Frame(left_frame, bg="white")
    book_data_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tk.Button(form_frame, text="Back to Welcome Page", command=welcome_page, bg="orange", fg="white", font=('Helvetica', 14)).pack(pady=10)

def member_page():
    clear_frame()
    set_background("image112.jpg")  

    tk.Label(top_frame, text="Member Details", font=('Helvetica', 30, 'bold'), bg="darkblue", fg="white").pack(pady=10, fill=tk.X)

    global member_id_var, name_var, phone_var, borrow_date_var, return_date_var, book_id_var
    member_id_var = tk.StringVar()
    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    borrow_date_var = tk.StringVar()
    return_date_var = tk.StringVar()
    book_id_var = tk.StringVar()

    
    form_frame = tk.Frame(left_frame, bg="white")
    form_frame.pack(pady=20, expand=True, anchor='center')

    
    create_labeled_entry("Member ID (For Update/Delete)", member_id_var, form_frame)
    create_labeled_entry("Name", name_var, form_frame)
    create_labeled_entry("Phone Number", phone_var, form_frame)
    create_labeled_entry("Borrow Date (YYYY-MM-DD)", borrow_date_var, form_frame)
    create_labeled_entry("Return Date (YYYY-MM-DD)", return_date_var, form_frame)
    create_labeled_entry("Book ID", book_id_var, form_frame)

    
    button_frame = tk.Frame(form_frame, bg="white")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Save", command=save_member, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Update", command=update_member, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete", command=delete_member, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Read", command=read_member, bg="orange", fg="white", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=5)

    
    global member_data_frame
    member_data_frame = tk.Frame(left_frame, bg="white")
    member_data_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tk.Button(form_frame, text="Back to Welcome Page", command=welcome_page, bg="orange", fg="white", font=('Helvetica', 14)).pack(pady=10)


def create_labeled_entry(label_text, variable, parent_frame):
    tk.Label(parent_frame, text=label_text, bg="white", fg="darkblue", font=('Helvetica', 12)).pack(pady=(10, 0))
    entry_frame = tk.Frame(parent_frame, bg="white")
    entry_frame.pack(pady=5)
    tk.Entry(entry_frame, textvariable=variable, width=40, font=('Helvetica', 12)).pack()  


def clear_frame():
    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.winfo_children():
        widget.destroy()
    for widget in top_frame.winfo_children():
        widget.destroy()


app = tk.Tk()
app.title("Library Management System")
app.geometry("1000x600")


top_frame = tk.Frame(app, bg="white")
top_frame.pack(side=tk.TOP, fill=tk.X)

left_frame = tk.Frame(app, width=400, bg="white")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(app, width=600, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


setup_database()
welcome_page()

app.mainloop()