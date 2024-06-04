"""
Tip Out App
Joseph Nelson Farrell
05-18-24

This file contains the EmployeeGUI class. This is the GUI that runs the employee database.
"""
# packages
import tkinter as tk
from tkinter import messagebox
import os
from classes.employee_database_class import EmployeeDatabase

# class def
class EmployeeGUI:
    def __init__(self, root, database):
        self.database = database
        self.root = root
        self.root.title("Employee Database Manager")
        self.root.geometry('400x200')  

        # create GUI elements
        tk.Label(self.root, text="First Name").grid(row=0, column=0)
        self.first_name_entry = tk.Entry(self.root, width=30)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Last Name").grid(row=1, column=0)
        self.last_name_entry = tk.Entry(self.root, width=30)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Email").grid(row=2, column=0)
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.grid(row=2, column=1)

        add_button = tk.Button(self.root, text="Add Employee", command=self.add_employee)
        add_button.grid(row=3, column=1, sticky=tk.W+tk.E, pady=4)

        remove_button = tk.Button(self.root, text="Remove Employee", command=self.remove_employee)
        remove_button.grid(row=4, column=1, sticky=tk.W+tk.E, pady=4)

        done_button = tk.Button(self.root, text="Done", command=self.root.destroy)
        done_button.grid(row=5, column=1, sticky=tk.W+tk.E, pady=4)

    def add_employee(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        if first_name and last_name and email:
            if not self.database.is_employee_in_file(self.database.name + ".csv", email):
                self.database.add_employee(last_name, first_name, email)
                messagebox.showinfo("Success", "Employee added successfully!")
                self.clear_fields() 
            else:
                messagebox.showerror("Error", "Employee with this email already exists!")
        else:
            messagebox.showerror("Error", "Please fill in all fields!")

    def remove_employee(self):
        """ Remove an employee from the database using the provided details """
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        if first_name and last_name and email:

            # Attempt to remove the employee
            if self.database.remove_employee(last_name, first_name, email):
                messagebox.showinfo("Success", "Employee removed successfully!")
            else:
                messagebox.showerror("Error", "No matching employee found to remove.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Please fill in all fields to remove an employee!")


    def clear_fields(self):
        """ Clear the input fields """
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    db = EmployeeDatabase("employee_information_database")
    app = EmployeeGUI(root, db)
    root.mainloop()
