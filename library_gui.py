import tkinter as tk
from tkinter import messagebox
import sqlite3

conn=sqlite3.connect("Library.db")
cursor=conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Library(
bookID INTEGER PRIMARY KEY,
name TEXT NOT NULL,
issued INTEGER DEFAULT 0

)""")

conn.commit()
conn.close()

def add_book():

    bookID=bookID_var.get()
    name=name_var.get()

    if bookID=="" or name=="":
        messagebox.showwarning(
        "Error",
        "Please fill all fields"
        )
        return
    
    conn=sqlite3.connect("Library.db")
    cursor=conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO Library VALUES (?,?,?)",(bookID,name,0)
        )
        conn.commit()

        messagebox.showinfo(
        "Success",
        "Book added successfully"
        )

        bookID_var.set("")
        name_var.set("")

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Book already exists"
        )
    
    conn.close()

def view_books():

    conn=sqlite3.connect("Library.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM Library")
    books=cursor.fetchall()
    conn.close()

    view_window=tk.Toplevel(window)
    view_window.title("All Books")
    view_window.geometry("500x500")

    if len(books)==0:
        tk.Label(
            view_window,
            text="No books Available"
        ).pack()

    else:
        for book in books:
            status="Available"

            if book[2]==1:
                status="Issued"

            text=(
                f"Title:{book[0]}\n"
                f"Author:{book[1]}\n"
                f"Status:{status}\n"
            )
            tk.Label(
                view_window,
                text=text
            ).pack()

def search_book():

    bookID=bookID_var.get()

    if bookID=="":
        messagebox.showwarning(
            "Warning",
            "Enter Book ID"
        ) 
        return

    conn=sqlite3.connect("Library.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM Library WHERE bookID=?",(bookID,))
    book=cursor.fetchone()
    conn.close()
    
    if book:
        status="Available"

        if book[2]==1:
            status="Issued"

    if book:
        messagebox.showinfo(
            "Book Found",
            f"BookID:{book[0]}\nBook name:{book[1]}\nStatus:{status}"
        )
    else:
        messagebox.showerror(
            "Error",
            "Book not found"
        )

def issue_book():
    bookID=bookID_var.get()

    if bookID=="":
        messagebox.showwarning(
            "Warning",
            "Enter BookID"
        )
        return

    conn=sqlite3.connect("Library.db")
    cursor=conn.cursor()

    cursor.execute(
        "SELECT * FROM Library WHERE bookID=?",(bookID,)
    )
    
    book=cursor.fetchone()

    if book is None:
        messagebox.showerror(
            "Error",
            "Book not found"
        )
    elif book[2]==1:
        messagebox.showwarning(
            "Warning",
            "Book already issued"
        )
    else:
        cursor.execute(
            "UPDATE Library SET issued=1 WHERE bookID=?",(bookID,)
        )
        conn.commit()

        messagebox.showinfo(
            "Status",
            "Book issued successfully"
            )

        conn.close()

def return_book():
    bookID=bookID_var.get()

    if bookID=="":
        messagebox.showwarning(
            "Warning",
            "Enter BookID"
        )
        return

    conn=sqlite3.connect("Library.db")
    cursor=conn.cursor()

    cursor.execute(
        "SELECT * FROM Library WHERE bookID=?",(bookID,)
    )
    
    book=cursor.fetchone()

    if book is None:
        messagebox.showerror(
            "Error",
            "Book not found"
        )
    elif book[2]==0:
        messagebox.showwarning(
            "Warning",
            "Book is already available"
        )
    else:
        cursor.execute("UPDATE Library SET issued=0 WHERE bookID=?",(bookID,))
        conn.commit()

        messagebox.showinfo(
            "Status",
            "Book returned successfully"
        )
    conn.close()

    
def delete_book():
    bookID=bookID_var.get()

    if bookID=="":
        messagebox.showwarning(
            "Warning",
            "Enter BookID"
        )
        return

    conn=sqlite3.connect("Library.db")
    cursor=conn.cursor()

    cursor.execute(
        "DELETE FROM Library WHERE bookID=?",(bookID,)
    )
    
    conn.commit()

    if cursor.rowcount==0:
        messagebox.showerror(
            "Error",
            "Book not found"
        )
    else:
        messagebox.showinfo(
            "Success",
            "Book deleted successfully"
        )
        bookID_var.set("")
        name_var.set("")
    conn.close()


window=tk.Tk()

window.title("Library management system")
window.geometry("500x500")

bookID_var=tk.StringVar()
name_var=tk.StringVar()

tk.Label(window,text="Book ID").grid(row=0,column=0,padx=10,pady=10)
tk.Label(window,text="Book Name").grid(row=1,column=0,padx=10,pady=10)

name_entry=tk.Entry(window,textvariable=bookID_var)
name_entry.grid(row=0,column=1)

author_entry=tk.Entry(window,textvariable=name_var)
author_entry.grid(row=1,column=1)

add_button=tk.Button(
    window,
    text="Add Book",
    command=add_book
)
add_button.grid(row=2,column=0,padx=10,pady=10)

view_button=tk.Button(
    window,
    text="View Books",
    command=view_books
)
view_button.grid(row=2,column=1,padx=10,pady=10)

search_button=tk.Button(
    window,
    text="Search Book",
    command=search_book
)
search_button.grid(row=2,column=2,padx=10,pady=10)

issue_button=tk.Button(
    window,
    text="Issue book",
    command=issue_book
)
issue_button.grid(row=3,column=0,padx=10,pady=10)

return_button=tk.Button(
    window,
    text="Return book",
    command=return_book
)
return_button.grid(row=3,column=1,padx=10,pady=10)

delete_button=tk.Button(
    window,
    text="Delete Book",
    command=delete_book
)
delete_button.grid(row=3,column=2,padx=10,pady=10)

window.mainloop()






