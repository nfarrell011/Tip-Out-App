""" 
    Tip Out Transparency Calculator & Data Manager
    This file contains
"""


import csv
import random
from datetime import timedelta, datetime
from pathlib import Path
import os

def generate_synthetic_data(filename):
    """
        This function will generate 2 weeks of synthetic employee data.

        Args:
            filename: (str) - the filename
    """
    # set paths
    PATH_TO_DATABASE_FOLDER = Path(os.getcwd()) / "employee_pay_database"
    PATH_TO_DATABASE_FOLDER.mkdir(parents = True, exist_ok = True)
    PATH_TO_DATABASE = PATH_TO_DATABASE_FOLDER / filename

    # names
    name_pairs = [
        ('Farrell', 'Nelson'),
        ('Fahey', 'Chris'),
        ('Doe', 'John'),
        ('Smith', 'Jane')
    ]

    # positions
    positions = ['Server', 'Host']
    shifts = ['DINNER', "LUNCH"]
    
    # date range for two weeks
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)  
    
    with open(PATH_TO_DATABASE, 'w', newline='') as file:

        # create writer
        writer = csv.writer(file)

        # write the header
        writer.writerow(['date', 'shift', 'last_name', 'first_name', 'position', 'hours', 'pay'])
        
        # generate data over the date range
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            for names in name_pairs:
                last_name, first_name = names
                position = random.choice(positions)
                shift = random.choice(shifts)
                hours = random.uniform(5, 12) 
                pay = random.uniform(80, 200)  
                
                # write the data row
                writer.writerow([date_str, shift, last_name, first_name, position, hours, round(pay, 2)])
            current_date += timedelta(days = 1)


generate_synthetic_data('synthetic_employee_data.csv')  

