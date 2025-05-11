import tkinter as tk
from tkinter import ttk

from backend.executor import DatabaseExecutor
from backend.connector import SQLConnector

def verify_phone_number(phone_number: str) -> bool:
    """
    Verifies if a phone number is valid
    :param phone_number: str: The phone number to verify
    :return: bool: True if the phone number is valid, False otherwise
    """
    if len(phone_number) != 10:  # check if the phone number is 10 digits long
        return False

    for char in phone_number:  # check if all characters in the phone number are digits
        if not char.isdigit():
            return False

    return True

def verify_email(email: str) -> bool:
    """
    Verifies if an email address is valid
    :param email: str: The email address to verify
    :return: bool: True if the email address is valid, False otherwise
    """
    if "@" not in email or "." not in email:  # check if the email address contains an @ and a .
        return False
    
    if not email.endswith(".com") and not email.endswith(".org"):  
        # check if the email address ends with .com or .org
        return False
    
    return True

def verify_date(date: str) -> bool:
    try:
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)
    except ValueError:
        return False
    
    if year < 0 or month < 1 or month > 12 or day < 1 or day > 31:
        return False
    
    return True

class SDCApp:
    """
    LibraryApp class, the main class for the library application. Responsible for creating the main window
    and managing the tabs for the application. Holds tabs for Books, Members, and Borrowings.
    """
    def __init__(self, app_name: str, window_width: int=500, window_height: int=500) -> None:
        self.__root = tk.Tk()
        self.__root.title(app_name)
        self.set_window_size(window_width, window_height)
        self.__notebook = ttk.Notebook(self.__root)

        # self.__admin_portal = AdminPortal(self.__notebook)

        self.__db_exec: DatabaseExecutor
        self.__username: str = ""

        self.handle_login()
        # self.__instructors_tab.create_books_tab()c
        # self.__instructors_tab.create_members_tab()
        # self.__borrow_tab.create_borrow_tab()
        self.__notebook.pack(expand=1, fill="both")

    def set_window_size(self, width: int, height: int) -> None:
        """
        Sets the size of the main window
        :param width: int: The width of the window
        :param height: int: The height of the window
        """
        self.__root.geometry(f"{width}x{height}")

    def handle_login(self) -> None:
        def __login():
            """
            Handles the login process. Checks if the username and password are correct.
            If they are, closes the login window and opens the main window.
            """
            username = username_entry.get()
            password = password_entry.get()

            try:
                db_conn = SQLConnector(
                    db_name="sdc-main",
                    port=33069,
                    host="localhost",
                    user=username,
                    password=password
                )
            except Exception as e:
                error_label.config(text=str(e))
                error_label.pack()
                return 
            
            self.__db_exec = DatabaseExecutor(db_conn)
            self.__username = username
            error_label.config(text="Login successful", fg="green")
            error_label.pack()

            if self.__username == "admin_global":
                username_entry.pack_forget()
                password_entry.pack_forget()
                username_label.pack_forget()
                password_label.pack_forget()
                login_button.pack_forget()
                error_label.pack_forget()
                # self.__admin_portal.create_admin_portal()


        username_label = tk.Label(self.__notebook, text="Username")
        username_entry = tk.Entry(self.__notebook)
        username_label.pack()
        username_entry.pack()

        password_label = tk.Label(self.__notebook, text="Password")
        password_entry = tk.Entry(self.__notebook, show="*")
        password_label.pack()
        password_entry.pack()

        login_button = tk.Button(self.__notebook, text="Login", command=__login)
        login_button.pack()

        error_label = tk.Label(self.__notebook, text="", fg="red")

    def mainloop(self) -> None:
        """
        Starts the mainloop for the application.
        """
        self.__root.mainloop()

def main():
    app = SDCApp("SDC Library")
    app.mainloop()

if __name__ == "__main__":
    main()

