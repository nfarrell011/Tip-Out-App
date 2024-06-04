"""
Tip Out App
Joseph Nelson Farrell
05-18-24

This file contains the Employee class used in TipOutApp
"""
class Employee:
    """
    Employee class; attributes and methods pertaining to an specific employee
    """
    def __init__(self, first_name: str, last_name: str) -> None:
        """
        Initializer

        Args:
            first_name: (str) - Employee first name.
            last_name: (str) - Employee last name.
        
        Returns: 
            None
        """
        self.first_name = first_name
        self.last_name = last_name
        self.hours = 0
        self.pay = 0
        self.position = None
        self.email = None

    def update_hours(self, hours: float) -> None:
        """
        Updates the employee hours attribute

        Args:
            hours: (float) - Number of hours worked.

        Returns:
            None
        """
        self.hours += hours

    def update_position(self, position: str) -> None:
        """
        Updates the employee position attribute

        Args:
            position: (str) - Employee position.

        Returns:
            None
        """
        self.position = position

    def update_email(self, email: str) -> None:
        """
        Updates the employee email attribute

        Args:
            position: (str) - Employee email.

        Returns:
            None
        """
        self.email = email


