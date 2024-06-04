"""
Tip Out App
Joseph Nelson Farrell
05-18-24

This file contains the EmployeeDatabase class used in TipOutApp.
"""
# packages
import csv
import os
from pathlib import Path
import sys

# class def
class EmployeeDatabase:
    """
    This class controls the employee database
    """
    def __init__(self, name: str) -> None:
        """
        Initializer

        Args:
            name: (str) - name of the db
        """
        self.name = name

    def check_folder_exists(self, folder_name: str) -> str:
        """ 
        Check if folder exists, create if not.
        """
        if getattr(sys, 'frozen', False):
            PATH = os.path.dirname(sys.executable)
        else:
            PATH = Path(os.getcwd())
        PATH_TO_FOLDER = Path(PATH) / folder_name
        PATH_TO_FOLDER.mkdir(parents = True, exist_ok = True)
        return str(PATH_TO_FOLDER)

    def check_file_exists(self, file_path: str) -> bool:
        """ 
        Check if a file exists
        """
        return Path(file_path).exists()

    def is_employee_in_file(self, file_path, email) -> bool:
        """ 
        Check if an employee is in the database. It uses "email" to perform the check. 
        """
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[2] == email:
                        return True
        except FileNotFoundError:
            return False
        return False

    def add_employee(self, last_name: str, first_name: str, email: str) -> None:
        """ 
        Add an employee to the employee database, if the employee is not already present 
        """
        database_folder = 'databases'
        database_folder_path = self.check_folder_exists(database_folder)
        database_file = self.name + ".csv"
        path_to_database = os.path.join(database_folder_path, database_file)

        with open(path_to_database, 'a' if self.check_file_exists(path_to_database) else 'w', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['last_name', 'first_name', 'email_address'])
            if not self.is_employee_in_file(path_to_database, email):
                writer.writerow([last_name, first_name, email])

    def remove_employee(self, last_name: str, first_name: str, email: str) -> bool:
        """ 
            This function will remove an employee based on matching last name, first name, and email. 
        """
        # set the path to the employee database
        database_folder = 'databases'
        database_folder_path = self.check_folder_exists(database_folder)
        database_file = self.name + ".csv"
        PATH_TO_DATABASE = os.path.join(database_folder_path, database_file)

        # data holders and flag
        updated_rows = []
        found = False
        try:
            # read all data and filter out the employee to be removed
            with open(PATH_TO_DATABASE, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:

                    # this will skip the employee to be removed, not append
                    if row and (row[0] == last_name) and (row[1] == first_name) and (row[2] == email):
                        found = True
                        continue
                    updated_rows.append(row)
                    
            # this will create csv without the employee to be removed
            with open(PATH_TO_DATABASE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)

        except FileNotFoundError:
            print("The Employee Database cannot be found!")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
        return found

