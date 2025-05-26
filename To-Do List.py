from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# ------------------- GLOBALS -------------------
tasks = []

# ------------------- DATABASE SETUP -------------------
connection = sql.connect('listOfTasks.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

# ------------------- FUNCTIONS -------------------

def add_task():
    task_string = task_field.get()
    if task_string.strip() == "":
        messagebox.showinfo('Error', 'Task field is empty!')
    else:
        tasks.append(task_string)
        cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_string,))
        task_field.delete(0, END)
        list_update()

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert(END, task)

def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        tasks.remove(selected_task)
        cursor.execute('DELETE FROM tasks WHERE title = ?', (selected_task,))
        list_update()
    except:
        messagebox.showinfo('Error', 'No task selected.')

def delete_all_tasks():
    confirm = messagebox.askyesno('Warning', 'Delete all tasks?')
    if confirm:
        tasks.clear()
        cursor.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, END)

def close_app():
    connection.commit()
    cursor.close()
    guiwindow.destroy()

def retrieve_database():
    tasks.clear()
    for row in cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

# ------------------- GUI SETUP -------------------

guiwindow = Tk()
guiwindow.title("To-Do List")
guiwindow.geometry("700x460+500+250")
guiwindow.resizable(False, False)
guiwindow.configure(bg="#B5E5CF")

# Frame
functions_frame = Frame(guiwindow, bg="#8EE5EE")
functions_frame.pack(expand=True, fill="both")

# Label
task_label = Label(functions_frame, text="TO-DO-LIST\nEnter the Task Title:", font=("arial", 14, "bold"), bg="#8EE5EE", fg="#FF6103")
task_label.place(x=20, y=30)

# Entry Field
task_field = Entry(functions_frame, font=("arial", 14), width=42, bg="white", fg="black")
task_field.place(x=220, y=30)

# Buttons
add_button = Button(functions_frame, text="Add", width=15, bg='#D4AC0D', font=("arial", 14, "bold"), command=add_task)
del_button = Button(functions_frame, text="Remove", width=15, bg='#D4AC0D', font=("arial", 14, "bold"), command=delete_task)
del_all_button = Button(functions_frame, text="Delete All", width=15, bg='#D4AC0D', font=("arial", 14, "bold"), command=delete_all_tasks)

add_button.place(x=30, y=90)
del_button.place(x=260, y=90)
del_all_button.place(x=490, y=90)

# Listbox
task_listbox = Listbox(functions_frame, width=90, height=10, font=("arial", 12), selectmode='SINGLE', bg="white", fg="black", selectbackground="#FF8C00", selectforeground="black")
task_listbox.place(x=30, y=150)

# Exit Button
exit_button = Button(functions_frame, text="Exit / Close", width=58, bg='#D4AC0D', font=("arial", 14, "bold"), command=close_app)
exit_button.place(x=30, y=390)

# ------------------- INIT -------------------
retrieve_database()
list_update()
guiwindow.mainloop()

        
        
        
        
        
        