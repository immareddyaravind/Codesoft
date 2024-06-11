import tkinter as tk
from tkinter import messagebox
import json
import os

TODO_FILE = 'todo_list.json'

def load_todo_list():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_todo_list(todo_list):
    with open(TODO_FILE, 'w') as file:
        json.dump(todo_list, file)

class ToDoApp:
    def _init_(self, root):
        self.root = root
        self.root.title("To-Do List Application")

        self.tasks = load_todo_list()
        self.task_var = tk.StringVar()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_entry = tk.Entry(self.frame, textvariable=self.task_var, width=50)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.tasks_listbox = tk.Listbox(root, width=75, height=15)
        self.tasks_listbox.pack(pady=10)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.update_button = tk.Button(self.buttons_frame, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.done_button = tk.Button(self.buttons_frame, text="Mark as Done", command=self.mark_task_done)
        self.done_button.pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def add_task(self):
        task_description = self.task_var.get()
        if task_description:
            task = {'description': task_description, 'done': False}
            self.tasks.append(task)
            save_todo_list(self.tasks)
            self.task_var.set("")
            self.refresh_listbox()
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty!")

    def update_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            new_description = self.task_var.get()
            if new_description:
                self.tasks[selected_task_index[0]]['description'] = new_description
                save_todo_list(self.tasks)
                self.task_var.set("")
                self.refresh_listbox()
            else:
                messagebox.showwarning("Input Error", "Task description cannot be empty!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to update!")

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            save_todo_list(self.tasks)
            self.refresh_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")

    def mark_task_done(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]['done'] = True
            save_todo_list(self.tasks)
            self.refresh_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done!")

    def refresh_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = 'Done' if task['done'] else 'Not Done'
            self.tasks_listbox.insert(tk.END, f"{task['description']} [{status}]")

if _name_ == "_main_":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
