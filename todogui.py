import tkinter as tk
from tkinter import messagebox

todos = []

root = tk.Tk()
root.title("Todo App")
root.geometry("400x600")

#switcher
def switch_to_main():
    welcome.place_forget()
    welcome_btns.pack_forget()
    main_page.pack(fill="both", expand=True)

def switch_to_welcome():
    main_page.pack_forget()
    welcome.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    welcome_btns.pack(side=tk.BOTTOM)

#first page
welcome = tk.Frame(root)

tk.Label(welcome, text="Welcome To T@PP", font=("Arial", 24)).pack()
tk.Label(welcome, text="part of the curiousity program").pack()

welcome.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

welcome_btns = tk.Frame(root, pady=20)
welcome_btns.pack(side=tk.BOTTOM)

btnsinit = tk.Button(welcome_btns, text="Get Started ...", 
                     height=1, width=40, command=switch_to_main)
btnsinit.pack()


main_page = tk.Frame(root)

td_total = tk.Label(main_page, text=f'Number Of Todos: {len(todos)}',font=("Arial", 14))
td_total.pack(padx=10, pady=10)


todo_display = tk.Frame(main_page)
todo_display.pack(pady=4)

for todo in todos:
    todo_frame = tk.Frame(todo_display, relief=tk.RIDGE, borderwidth=1, padx=4, pady=5)
    todo_frame.pack(fill="x", padx=10, pady=5)
    td_item = tk.Label(todo_frame, text=f'Task: {todo["text"]}', font=("Arial", 12))
    td_item.pack(anchor="w")
    status_text = "Complete" if todo["status"] else "Incomplete"
    td_status = tk.Label(todo_frame, text=f'Status: {status_text}')
    td_status.pack(anchor="w")

# nt
input_frame = tk.Frame(main_page)
input_frame.place(rely=0.8,relx=0.5,anchor=tk.CENTER )

tk.Label(input_frame, text="Add New Todo:").pack()
todo_entry = tk.Entry(input_frame, width=30)
todo_entry.pack(pady=5)

def add_todo():
    text = todo_entry.get()
    if text:
        new_todo = {
            "id": len(todos) + 1,
            "text": text,
            "status": False
        }
        todos.append(new_todo)
        todo_entry.delete(0, tk.END)
        messagebox.askokcancel("Success", "Todo added!")
        refresh_todos()
        todoLimiter()
    else:
        messagebox.showwarning("Empty", "Please enter a todo!")

def refresh_todos():
    for widget in todo_display.winfo_children():
        widget.destroy()
    for todo in todos:
        todo_frame = tk.Frame(todo_display, relief=tk.RIDGE, borderwidth=1, padx=10, pady=5)
        todo_frame.pack(fill="x", padx=10, pady=5)
        td_item = tk.Label(todo_frame, text=f'Task: {todo["text"]}', font=("Arial", 12))
        td_item.pack(anchor="w")
        status_text = "Complete" if todo["status"] else "Incomplete"
        td_status = tk.Label(todo_frame, text=f'Status: {status_text}')
        td_status.pack(anchor="w")
    td_total.config(text=f'Number Of Todos: {len(todos)}')

def todoLimiter():
    if len(todos) >= 2:
        todo_btnsADD.pack_forget()
        messagebox.showwarning("ex0001","limit of 5 todos reached")
def todo_deleter():
    for todo in todos:
        todos.pop()
    refresh_todos()
    todo_btnsADD.pack()

todo_btnsADD = tk.Button(input_frame, text="Add Todo", command=add_todo, width=20)
todo_btnsADD.pack(pady=2)

todo_reset = tk.Button(input_frame, text="reset",width=20 , command=todo_deleter)
todo_reset.pack(side=tk.BOTTOM)
root.mainloop()
