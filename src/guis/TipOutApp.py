"""
Tip Out App
Joseph Nelson Farrell
05-18-24

This file contains the TipOut Class.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import traceback
import sys
from pathlib import Path

PATH_TO_CLASSES = Path.cwd() / "src"
sys.path.append(str(PATH_TO_CLASSES))

from classes.employee_class import Employee
from classes.tip_out_class import TipOut, update_sender_email_info
from classes.employee_database_class import EmployeeDatabase
from guis.employee_database_driver_gui import EmployeeGUI

class TipOutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Tip Out Calculator")
        self.root.iconbitmap('/Users/nelsonfarrell/Documents/Northeastern/projects/tip_out_calc/output.icns')
        self.tip_out = None
        self.date = None
        self.shift = None
        self.employees = []
        self.total_tips_entry = None
        self.host_tip_percent_entry = None
        self.result_label = None
        self.employees_display = None
        self.root.withdraw()

    def update_date_shift_window(self):
        top = tk.Toplevel(self.root)
        top.title("Update Date and Shift")
        top.geometry('500x150')
        top.grab_set()

        tk.Label(top, text="Enter Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        date_entry = tk.Entry(top, width=20)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top, text="Select Shift:").grid(row=1, column=0, padx=10, pady=5)
        shift_combo = ttk.Combobox(top, values=["lunch", "dinner"], width=18)
        shift_combo.grid(row=1, column=1, padx=10, pady=5)

        submit_button = tk.Button(top, text="Update", command=lambda: self.submit_date_shift(date_entry.get(), shift_combo.get(), top))
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def submit_date_shift(self, date, shift, window):
        if shift not in ["lunch", "dinner"]:
            messagebox.showerror("Error", "Please select a valid shift: 'lunch' or 'dinner'.")
            return
        if not date:
            messagebox.showerror("Error", "Please enter a valid date in the format YYYY-MM-DD.")
            return
        self.date = date
        self.shift = shift
        window.destroy()
        self.root.deiconify()
        self.setup_main_gui()

    def load_names(self):
        names = []
        if getattr(sys, 'frozen', False):
            PATH = os.path.dirname(sys.executable)
        else:
            PATH = Path(os.getcwd())
        PATH_TO_EMPLOYEE_DATABASE = os.path.join(PATH, "databases", "employee_information_database.csv")
        try:
            with open(PATH_TO_EMPLOYEE_DATABASE, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                for row in reader:
                    name = f"{row[0]} {row[1]}"  
                    names.append(name)
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", "You must add employees to the employee database first!")
            return False
        return names

    def add_employee_window(self):
        names = self.load_names()
        if names == False:
            return
        top = tk.Toplevel()
        top.title("Add New Shift Employee")
        top.geometry('500x200')  

        # set min size
        top.minsize(300, 200)

        # name dropdown
        tk.Label(top, text="Name:").grid(column=0, row=0, sticky='e', padx=10, pady=5)
        name_combo = ttk.Combobox(top, values=names, width=25)
        name_combo.grid(column=1, row=0, padx=10, pady=5)
        
        # hours entry
        tk.Label(top, text = "Hours Worked:").grid(column=0, row=1, sticky='e', padx=10, pady=5)
        hours_entry = tk.Entry(top, width=25)
        hours_entry.grid(column=1, row=1, padx=10, pady=5)

        # position dropdown
        tk.Label(top, text="Position:").grid(column=0, row=2, sticky='e', padx=10, pady=5)
        position_combo = ttk.Combobox(top, values=["server", "host"], width=22)
        position_combo.grid(column=1, row=2, padx=10, pady=5)

        # save employee button
        save_button = tk.Button(top, text="Save Employee", command=lambda: self.save_employee(name_combo, hours_entry, position_combo, top))
        save_button.grid(column=1, row=3, padx=10, pady=10, sticky='ew')

    def save_employee(self, name_combo, hours_entry, position_combo, window):
        name = name_combo.get()
        hours = hours_entry.get()
        position = position_combo.get()
        if name and hours and position:
            last_name, first_name = name.split()[:2] 
            emp = Employee(first_name, last_name)
            emp.update_hours(float(hours))
            emp.update_position(position)
            self.employees.append(emp)
            self.employees_display.config(state=tk.NORMAL)
            entry = f"{first_name} {last_name}, Hours: {hours}, Position: {position}\n"
            self.employees_display.insert(tk.END, entry)
            self.employees_display.config(state=tk.DISABLED)
        window.destroy()

    def on_entry_click_total_tips(self, event, entry, default_text):
        """
            Function to be called when the entry is clicked for total tips
        """
        if entry.get() == default_text:
            entry.delete(0, "end")  # delete all the text in the entry
            entry.insert(0, '')  # Insert blank for user input
            entry.config(fg='black')

    def on_focusout_total_tips(self, event, entry, default_text):
        """
            Function to be called when the entry loses focus for total tips
        """
        if entry.get() == '':
            entry.insert(0, default_text)
            entry.config(fg='grey')

    def on_entry_click_host_percent(self, event, entry, default_text):
        """
            Function to be called when the entry is clicked for host percent
        """
        if entry.get() == default_text:
            entry.delete(0, "end")  # delete all the text in the entry
            entry.insert(0, '')  # Insert blank for user input
            entry.config(fg='black')

    def on_focusout_host_percent(self, event, entry, default_text):
        """
            Function to be called when the entry loses focus for host percent
        """
        if entry.get() == '':
            entry.insert(0, default_text)
            entry.config(fg='grey')

    def calculate_tips(self):
        self.tip_out = TipOut(self.employees)
        self.tip_out.date = self.date
        self.tip_out.shift = self.shift
        self.tip_out.update_total_tips(float(self.total_tips_entry.get()))
        self.tip_out.update_total_hours()
        self.tip_out.get_host_tip_out(float(self.host_tip_percent_entry.get()))
        self.tip_out.get_server_hourly()
        self.tip_out.update_server_pay()

        result_text = '\n'.join(f"{emp.first_name} {emp.last_name} - ${emp.pay:.2f}" for emp in self.employees)
        self.result_label.config(text = result_text)
        return self.tip_out

    def generate_pdf(self):
        try:
            self.tip_out.generate_daily_payout_report()
            messagebox.showinfo("Report Generated", "The PDF report has been successfully generated.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate the report: {str(e)}")
        return self.tip_out

    def prompt_for_dates(self):

        # create a pop-up window
        date_window = tk.Toplevel(self.root)
        date_window.title("Enter Dates for Report")

        # add labels and entry widgets for start and end dates
        tk.Label(date_window, text="Enter Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        start_date_entry_popup = tk.Entry(date_window, width=25)
        start_date_entry_popup.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(date_window, text="Enter End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        end_date_entry_popup = tk.Entry(date_window, width=25)
        end_date_entry_popup.grid(row=1, column=1, padx=10, pady=10)

        # this function will get the date entries
        def submit_dates():
            start_date = start_date_entry_popup.get()
            end_date = end_date_entry_popup.get()
            date_window.destroy()  # close window
            self.generate_weekly_report(start_date, end_date)  # Call the report generation function with dates

        # Button to submit dates
        submit_button = tk.Button(date_window, text="Generate Report", command=submit_dates)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def generate_weekly_report(self, start_date, end_date):
        try:
            # validate the date format and that the entries are not the default text
            if start_date.count('-') != 2 or end_date.count('-') != 2 or 'Enter' in start_date or 'Enter' in end_date:
                messagebox.showerror("Error", "Please enter valid dates in the format YYYY-MM-DD.")
                return

            print(f"Generating report from {start_date} to {end_date}")
            self.tip_out.generate_weekly_pay_report(start_date, end_date)
            messagebox.showinfo("Success", "Report generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_employee_pay_database(self):
        try:
            self.tip_out.update_employee_pay_database()
            messagebox.showinfo("Database Updated", "The employee database has been successfully updated.")
        except Exception as e:
            traceback.print_exc()
            print("Hello")
            messagebox.showerror("Error!", f"Failed to update Employee Pay Database: {str(e)}")

    def popup_update_sender_email(self):

        # Create a top-level window
        top = tk.Toplevel()
        top.title("Update Sender Email")
        top.geometry('450x150')  # Smaller window size

        # Email entry
        tk.Label(top, text="Sender Email:").grid(row=0, column=0, padx=10, pady=5)
        email_entry = tk.Entry(top, width=25)
        email_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password entry
        tk.Label(top, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(top, width=25, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Function to update the email and password
        def submit_sender_info():
            sender_email = email_entry.get()
            sender_password = password_entry.get()
            update_sender_email_info(sender_email, sender_password)
            top.destroy()  # Close the window after submission

        # Submit button
        submit_button = tk.Button(top, text="Update Email", command=submit_sender_info)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def gui_send_emails(self):
        report = self.tip_out.get_todays_report() 
        email_addresses = self.tip_out.fetch_and_update_email()
        self.tip_out.get_sender_email_info()
        self.tip_out.send_emails(report, email_addresses)
        messagebox.showinfo("Email Sent", "The report has been sent successfully to all listed emails.")

    def modify_employee_database(self):
        new_window = tk.Tk()
        db = EmployeeDatabase("employee_information_database")
        EmployeeGUI(new_window, db)

    def setup_main_gui(self):
        self.root.title("Dynamic Tip Out Calculator")
        #self.root.iconbitmap('/Users/nelsonfarrell/Documents/Northeastern/projects/tip_out_calc/output.icns')  

        # Main frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack()

        # Button to add new employee window
        add_button = tk.Button(control_frame, text="Add Shift Employee", command= self.add_employee_window)
        add_button.grid(column=0, row=0, columnspan=2)

        # Initialize the Text widget to display employee info
        self.employees_display = tk.Text(control_frame, height=10, width=50)
        self.employees_display.grid(column=0, row=2, columnspan=2, pady=5, padx=5)
        self.employees_display.insert(tk.END, "\t\t Shift Employees:\n")
        self.employees_display.config(state=tk.DISABLED)  # Disable editing of the text widget

        # this will enter the database GUI, allowing the user to add or remove employees
        modify_db_button = tk.Button(control_frame, text="Modify Employee Database", command = self.modify_employee_database)
        modify_db_button.grid(column=3, row=0, columnspan = 2, pady = 10)

        pdf_button = tk.Button(control_frame, text="Generate Weekly Summary Report", command = self.prompt_for_dates)
        pdf_button.grid(column=3, row=3, columnspan=2, pady=10, padx=5)

        # total tips entry field
        self.total_tips_entry = tk.Entry(control_frame, width=25)
        self.total_tips_entry.insert(0, 'Enter Total Tips')
        self.total_tips_entry.config(fg='grey')
        self.total_tips_entry.bind('<FocusIn>', lambda event, e=self.total_tips_entry, d='Enter Total Tips': self.on_entry_click_total_tips(event, e, d))
        self.total_tips_entry.bind('<FocusOut>', lambda event, e=self.total_tips_entry, d='Enter Total Tips': self.on_focusout_total_tips(event, e, d))
        self.total_tips_entry.grid(column=0, row=3)

        # host tip out percent entry field
        self.host_tip_percent_entry = tk.Entry(control_frame, width=25)
        self.host_tip_percent_entry.insert(0, 'Enter Host Tip Out Percentage')
        self.host_tip_percent_entry.config(fg='grey')
        self.host_tip_percent_entry.bind('<FocusIn>', lambda event, e=self.host_tip_percent_entry, d='Enter Host Tip Out Percentage': self.on_entry_click_host_percent(event, e, d))
        self.host_tip_percent_entry.bind('<FocusOut>', lambda event, e=self.host_tip_percent_entry, d='Enter Host Tip Out Percentage': self.on_focusout_host_percent(event, e, d))
        self.host_tip_percent_entry.grid(column=0, row=4)

        # Button to calculate tips
        calc_button = tk.Button(control_frame, text="Calculate Tips", command = self.calculate_tips)
        calc_button.grid(column=0, row=8, columnspan=2)

        # Label to display results
        self.result_label = tk.Label(control_frame, text="", font=('Arial', 10))
        self.result_label.grid(column=0, row=9, columnspan=2)

        # Button to generate and view the PDF report
        pdf_button = tk.Button(control_frame, text="Generate PDF Report", command = self.generate_pdf)
        pdf_button.grid(column=0, row=12, columnspan=2, pady=10)

        # Button to generate and view the PDF report
        pdf_button = tk.Button(control_frame, text="Update Employee Pay Database", command = self.update_employee_pay_database)
        pdf_button.grid(column=0, row=13, columnspan=2, pady=10)

        # Add a button in the main GUI to open the update email popup
        update_email_button = tk.Button(control_frame, text="Update Sender Email", command = self.popup_update_sender_email)
        update_email_button.grid(column=3, row=14, columnspan=2, pady=10)

        email_button = tk.Button(control_frame, text="Send Emails", command= self.gui_send_emails)
        email_button.grid(column=0, row=14, columnspan=2, pady=10)

        # Button to close the application
        close_button = tk.Button(control_frame, text="Close Application", command = self.root.destroy)
        close_button.grid(column=0, row=15, columnspan=2, pady=10)

    def main_app(self):

        # Initially open the window to update date and shift
        self.update_date_shift_window()
        self.root.mainloop()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = TipOutApp(root)
    app.main_app()