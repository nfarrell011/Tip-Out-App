"""
Tip Out App
Joseph Nelson Farrell
05-18-24

This file contains the TipOut Class.
"""
# packages
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import datetime
import os
import smtplib
import certifi
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import ssl
from pathlib import Path
import pandas as pd
import sys

# class def
class TipOut:
    """
        This class will compute tip-outs, generate reports (pdfs), update databases, and 
        distribute reports via email. 
    """
    def __init__(self, employees: list) -> None:
        self.employees = employees 
        self.total_tips = 0
        self.total_hours = 0
        self.server_hourly = 0
        self.host_hourly = 0
        self.total_host_hours = 0
        self.total_tips_post_host = 0
        self.total_host_tipout = 0
        self.shift = None
        self.date = None

    def update_total_tips(self, total_tips):
        """
            This function will update "total_tips" attribute.

            Args:
                total_tips: (int) - the total tips taken in by the house
        """
        self.total_tips += total_tips

    def update_total_hours(self):
        """
            This function will update "total_hours" attribute.
        """
        total_hours = 0
        for employee in self.employees:
            if employee.position == "server":
                total_hours += employee.hours
        self.total_hours = total_hours

    def update_date_shift(self, date, shift):
        self.date = date
        self.shift = shift
                
    def get_host_tip_out(self, tip_out_percent):
        """
            This function will compute the tip out for the hosts.
        """
        host_list = []
        for employee in self.employees:
            if employee.position == 'host':
                host_list.append(employee)
        num_hosts = len(host_list)
        if num_hosts == 0:
            self.total_tips_post_host = self.total_tips
            return "There were no hosts on tonight"
        
        else:
            # get host tip out
            total_host_tip_out = self.total_tips * (tip_out_percent/100)
            self.total_host_tipout = total_host_tip_out

            # get host hours
            total_host_hours = 0
            for host in host_list:
                total_host_hours += host.hours
            self.total_host_hours = total_host_hours

            # get host hourly
            host_hourly = total_host_tip_out / total_host_hours
            self.host_hourly = host_hourly

            # update host pay
            for host in host_list:
                host.pay = host.hours * host_hourly

            self.total_tips_post_host = round((self.total_tips - total_host_tip_out), 4)

    def get_server_hourly(self):
        """
            This function will compute the server hourly.
        """
        server_hourly = self.total_tips_post_host / self.total_hours
        self.server_hourly = round(server_hourly, 4)

    def update_server_pay(self):
        """
            The function will update the pay for individual servers.
        """
        for employee in self.employees:
            if employee.position == "server":
                employee.pay = round((employee.hours * self.server_hourly), 4)


    def update_employee_pay_database(self):
        """
            This function will update the employee pay database.
        """
        if getattr(sys, 'frozen', False):
            PATH = os.path.dirname(sys.executable)
        else:
            PATH = Path(os.getcwd())
        # set paths
        PATH_TO_DATABASE_FOLDER = Path(PATH) / "databases"
        PATH_TO_DATABASE_FOLDER.mkdir(parents = True, exist_ok = True)
        PATH_TO_DATABASE = PATH_TO_DATABASE_FOLDER / "employee_pay_database.csv"

        # get the current date
        current_datetime = datetime.date.today()
        current_datetime = str(current_datetime)

        # iterate over employees who were working
        for employee in self.employees:
            first_name = employee.first_name
            last_name = employee.last_name
            pay = employee.pay
            hours = employee.hours
            position = employee.position
            shift = self.shift
            date = self.date 

            # open and update the database csv
            with open(PATH_TO_DATABASE, 'a', newline = '') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(['date', 'shift', 'last_name', 'first_name', 'position', 'hours', 'pay'])
                writer.writerow([date, shift, last_name, first_name, position, hours, pay])

    def generate_weekly_pay_report(self, start_date, end_date):
        """
            This function will generate a pdf report summarizing employee hours and pay defined by the date range
            arguements

            args:
                start_date: (str) - the report start date.
                end_date: (str) - the report end date. 
        """
        if getattr(sys, 'frozen', False):
            PATH = Path(os.path.dirname(sys.executable))
        else:
            PATH = Path(os.getcwd())

        PATH_TO_DATABASE_FOLDER = os.path.join(PATH, "databases")
        PATH_TO_DATABASE = os.path.join(PATH_TO_DATABASE_FOLDER, "employee_pay_database.csv")

        PATH_TO_INSIGNIA = os.path.join(PATH, "figs", "insignia.png")

        REPORTS_FOLDER_PATH = os.path.join(PATH, "reports", "weekly")

        # generate report save path
        REPORT_FILE_PATH = os.path.join(REPORTS_FOLDER_PATH, f"weekly_report_ending_{str(end_date)}.pdf")
        
        if not os.path.exists(REPORTS_FOLDER_PATH):
            os.makedirs(REPORTS_FOLDER_PATH)

        # convert dates to datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # get the current date
        current_datetime = datetime.date.today()
        current_datetime = str(current_datetime)

        # get and filter the employee database
        df = pd.read_csv(PATH_TO_DATABASE)
        df['date'] = pd.to_datetime(df['date'])
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        grouped_df = filtered_df.groupby(['last_name', 'first_name'])[['pay', 'hours']].sum()
        grouped_df['hours'] = grouped_df['hours'].round(2)
        grouped_df.reset_index(inplace = True)

        # make pdf
        c = canvas.Canvas(REPORT_FILE_PATH, pagesize = letter)
        width, height = letter  # Get the default size of the letter

        # add the date
        c.setFont("Helvetica", 12)
        c.drawString(400, 730, f'Report Generated on: {current_datetime}')

        # add david's insignia
        c.drawImage(PATH_TO_INSIGNIA, 70, 700, width = 100, height = 50) 

        # add the title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 630, "Weekly Pay Report")
        c.line(200, 625, 340, 625)

        # settings for the cols
        columns = ['Last Name', 'First Name', 'Total Hours', 'Total Pay']
        column_positions = [75, 175, 275, 375]  # x coordinates for each column
      
        # draw the headers
        start_height = 575
        c.setFont("Helvetica-Bold", 12)
        for col_pos, col_name in zip(column_positions, columns):
            c.drawString(col_pos, start_height, col_name)
        
        # draw the rows
        c.setFont("Helvetica", 12)
        start_height -= 20

        # get row data from grouped_df
        for index, row in grouped_df.iterrows():
            last_name = row['last_name']
            first_name = row['first_name']
            hours = round(row['hours'], 2)
            pay = round(row['pay'], 2)

            # drawing row data
            row_data = [last_name, first_name, str(hours), str(pay)]
            for col_pos, data in zip(column_positions, row_data):
                c.drawString(col_pos, start_height, data)
            start_height -= 20  # decrease height for the next row

        # save the PDF file
        c.showPage()
        c.save()


    def generate_daily_payout_report(self):
        """
            This function will generate a daily summary report pddf
        """
        # get the current date
        #current_datetime = datetime.date.today()
        #current_datetime = str(current_datetime)
        current_datetime = self.date
        shift = self.shift
        shift = shift.upper()

        # path to insignia
        if getattr(sys, 'frozen', False):
            PATH = Path(os.path.dirname(sys.executable))
        else:
            PATH = Path(os.getcwd())

        PATH_TO_INSIGNIA = os.path.join(PATH, "figs", "insignia.png")

        # path to reports folder
        REPORTS_FOLDER_PATH = os.path.join(PATH, "reports", "daily")
        
        # report file name
        REPORT_FILE_PATH = os.path.join(REPORTS_FOLDER_PATH, f"tip_out_report_{shift}_{current_datetime}.pdf")

        # make sure folder exists
        if not os.path.exists(REPORTS_FOLDER_PATH):
            os.makedirs(REPORTS_FOLDER_PATH)

        # create pdf
        c = canvas.Canvas(REPORT_FILE_PATH, pagesize=letter)
        width, height = letter 

        # add the date
        c.setFont("Helvetica", 12)
        c.drawString(455, 730, current_datetime)

        # add the shift
        c.setFont("Helvetica", 12)
        c.setFillColor((1, 0, 0))
        c.drawString(455, 710, shift)
        c.setFillColor((0, 0, 0))

        # add the insignia
        c.drawImage(PATH_TO_INSIGNIA, 70, 700, width = 100, height = 50) 

        # add the title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 630, "Tip Out Summary Report")

        # add totals
        c.setFont("Helvetica-Bold", 12)
        c.drawString(75, 600, "Total Tips: ")
        c.drawString(150, 600, str(self.total_tips))
        c.drawString(75, 580, "Host Tips: ")
        c.drawString(150, 580, str(self.total_host_tipout))
        c.drawString(75, 560, "Total Server Hours: ")
        c.drawString(195, 560, str(self.total_hours))
        c.drawString(75, 540, "Server Hourly: ")
        c.drawString(168, 540, str(self.server_hourly))
        c.drawString(75, 520, "Total Host Hours: ")
        c.drawString(195, 520, str(self.total_host_hours))
        c.drawString(75, 500, "Host Hourly: ")
        c.drawString(168, 500, str(self.host_hourly))


        # add col headers
        start_height = 450
        c.setFont("Helvetica-Bold", 12)
        c.drawString(75, start_height, "Last Name")
        c.drawString(175, start_height, "First Name")
        c.drawString(275, start_height, "Position")
        c.drawString(350, start_height, "Hours")
        c.drawString(425, start_height, "Tip Out")
        start_height -= 20

        # add data
        c.setFont("Helvetica", 12)
        for employee in self.employees:
            first_name = employee.first_name
            last_name = employee.last_name
            pay = employee.pay
            hours = employee.hours
            position = employee.position
            c.drawString(75, start_height, last_name)
            c.drawString(175, start_height, first_name)
            c.drawString(275, start_height, position)
            c.drawString(350, start_height, str(hours))
            c.drawString(425, start_height, str(pay))
            start_height -= 20

        # draw a line
        c.line(200, 625, 390, 625)

        # save the PDF file
        c.showPage()
        c.save()

    def fetch_and_update_email(self):
        """ 
            Fetch and update the email addresses for all employees from the CSV database. 
        """
        # set the paths
        if getattr(sys, 'frozen', False):
            PATH = Path(os.path.dirname(sys.executable))
        else:
            PATH = Path(os.getcwd())

        PATH_TO_DATABASE = os.path.join(PATH, "databases", "employee_information_database.csv")
        for employee in self.employees:
            with open(PATH_TO_DATABASE, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and (row[0] == employee.last_name) and (row[1] == employee.first_name):
                        employee.email = row[2]
                        break
        email_addresses = []
        for employee in self.employees:
            email = employee.email
            email_addresses.append(email)

        return email_addresses

    def get_todays_report(self):
    
        # set the paths
        if getattr(sys, 'frozen', False):
            PATH = Path(os.path.dirname(sys.executable))
        else:
            PATH = Path(os.getcwd())

        PATH_TO_REPORTS = os.path.join(PATH, "reports", "daily")

        # get the current date
        current_datetime = self.date
        shift = self.shift.upper()

        # iterate over files
        for filename in os.listdir(PATH_TO_REPORTS):
            if current_datetime in filename and shift in filename:
                return filename
            
    def get_sender_email_info(self):
            
            # set paths
            if getattr(sys, 'frozen', False):
                PATH = Path(os.path.dirname(sys.executable))
            else:
                PATH = Path(os.getcwd())
            
            PATH_TO_DATABASE = os.path.join(PATH, "databases", "report_sender_email_database.csv")

            with open(PATH_TO_DATABASE, "r", newline = '') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.sender_email = row[0]
                    self.sender_email_password = row[1]

            return None

    def send_emails(self, report, email_addresses):

        if getattr(sys, 'frozen', False):
            PATH = Path(os.path.dirname(sys.executable))
        else:
            PATH = Path(os.getcwd())

        PATH_TO_PDF = os.path.join(PATH, "reports", "daily", report)

        receiver = ",".join(email_addresses)

        subject = "Tip Out Summary Report"

        body = "Attached is the Tip Out Summary Report"

        em = EmailMessage()

        em['From'] = self.sender_email #sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)
        em.make_mixed()

        with open(PATH_TO_PDF, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                f"attachment; filename= {PATH_TO_PDF}")
            em.attach(part)

        context = ssl.create_default_context(cafile = certifi.where())

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
            smtp.login(self.sender_email, self.sender_email_password)
            smtp.send_message(em)

################## HELPER FUNCTION ###########################
def update_sender_email_info(sender_email, sender_password):

    # set paths
    if getattr(sys, 'frozen', False):
        PATH = Path(os.path.dirname(sys.executable))
    else:
        PATH = Path(os.getcwd())
    
    PATH_TO_DATABASE = os.path.join(PATH, "databases", "report_sender_email_database.csv")

    # open and update the database csv
    with open(PATH_TO_DATABASE, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([sender_email, sender_password])