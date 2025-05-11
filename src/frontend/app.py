import tkinter as tk
from tkinter import ttk

from backend.load.executor import DatabaseExecutor
from backend.load.connector import SQLConnector
from admin_portal import AdminPortal
from instructor_portal import InstructorPortal

class SDCApp:
    """
    LibraryApp class, the main class for the library application. Responsible for creating the main window
    and managing the tabs for the application. Holds tabs for Books, Members, and Borrowings.
    """
    def __init__(self, app_name: str, window_width: int=500, window_height: int=500) -> None:
        self.__app_name = app_name
        self.__window_width = window_width
        self.__window_height = window_height
        
        self.__admin_portal: AdminPortal
        self.__instructors_tab: InstructorPortal
        self.__logout_button: tk.Button
    
        self.__db_exec: DatabaseExecutor
        self.__username: str = ""

        self.__root = tk.Tk()
        self.__root.title(self.__app_name)

        self.app_home()

    def app_home(self) -> None:
        self.set_window_size(self.__window_width, self.__window_height)
        self.__notebook = ttk.Notebook(self.__root)

        self.handle_login()
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

            username_entry.pack_forget()
            password_entry.pack_forget()
            username_label.pack_forget()
            password_label.pack_forget()
            login_button.pack_forget()
            error_label.pack_forget()

            if self.__username == "admin_global":
                self.__admin_portal = AdminPortal(self.__db_exec, self.__notebook)
            elif self.__username == "instructor_global":
                self.__instructors_tab = InstructorPortal(self.__db_exec, self.__notebook)

            self.__logout_button = tk.Button(self.__root, text="Logout", command=self.handle_logout)
            self.__logout_button.pack(side="top", anchor="ne")

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

    def handle_logout(self) -> None:
        """
        Handles the logout process. Closes the main window and opens the login window.
        """
        self.__notebook.pack_forget()
        self.__logout_button.pack_forget()
        self.app_home()

    def mainloop(self) -> None:
        """
        Starts the mainloop for the application.
        """
        self.__root.mainloop()

def main():
    app = SDCApp("Smooth Driving College of Motoring Portal", 1200, 800)
    app.mainloop()

if __name__ == "__main__":
    main()

