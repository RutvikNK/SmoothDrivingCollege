import tkinter as tk
from tkinter import ttk

from backend.load.executor import DatabaseExecutor
from backend.load.connector import SQLConnector
from backend.data.sdc_data import (
    Employee,
    Office,
    Client,
    Vehicle,
    Interview,
    Meeting
)

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

        self.__db_exec: DatabaseExecutor
        self.__username: str = ""
        
        self.__admin_portal: AdminPortal

        self.handle_login()
        # self.__instructors_tab.create_vehicles_tab()c
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

                self.__admin_portal = AdminPortal(self.__db_exec, self.__notebook)


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

class AdminPortal:
    def __init__(self, exec: DatabaseExecutor, notebook: ttk.Notebook) -> None:
        self.__exec = exec
        self.__notebook = notebook

        self.__manage_inst_tab = ManageInstructorsTab(self.__exec, self.__notebook)
        self.__manage_client_tab = ManageClientsTab(self.__exec, self.__notebook)
        self.__manage_vehicle_tab = ManageVehiclesTab(self.__exec, self.__notebook)

        self.__manage_inst_tab.create_emps_tab()
        self.__manage_client_tab.create_clients_tab()
        self.__manage_vehicle_tab.create_vehicles_tab()

        self.__notebook.pack()

        # Add widgets for the admin portal here

class ManageInstructorsTab:
    def __init__(self, exec: DatabaseExecutor, notebook: ttk.Notebook) -> None:
        self.__exec = exec
        self.__notebook = notebook

        self.__active_tab = ""

    def show_emp_tab_labels(self, menu_to_show: str) -> None:
        """
        Shows the menu for the give book submenu
        :param menu_to_show: str: The submenu to show
        """
        self.__active_tab = menu_to_show
        if self.__active_tab == "add":  # show add employee submenu
            self.__name_label = tk.Label(self.__instructors_tab, text="Full Name: ")
            self.__name_label.place(relx=0.37, rely=0.2, anchor=tk.CENTER)
            self.__name_entry = tk.Entry(self.__instructors_tab)
            self.__name_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__gender_label = tk.Label(self.__instructors_tab, text="Gender: ")
            self.__gender_label.place(relx=0.37, rely=0.3, anchor=tk.CENTER)
            self.__gender_entry = tk.Entry(self.__instructors_tab)
            self.__gender_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

            self.__phone_label = tk.Label(self.__instructors_tab, text="Phone Number: ")
            self.__phone_label.place(relx=0.37, rely=0.4, anchor=tk.CENTER)
            self.__phone_entry = tk.Entry(self.__instructors_tab)
            self.__phone_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

            self.__email_label = tk.Label(self.__instructors_tab, text="Email Address: ")
            self.__email_label.place(relx=0.37, rely=0.5, anchor=tk.CENTER)
            self.__email_entry = tk.Entry(self.__instructors_tab)
            self.__email_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            self.__manager_id_label = tk.Label(self.__instructors_tab, text="Manager ID: ")
            self.__manager_id_label.place(relx=0.37, rely=0.6, anchor=tk.CENTER)
            self.__manager_id_entry = tk.Entry(self.__instructors_tab)
            self.__manager_id_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

            self.__add_emp_button = tk.Button(self.__instructors_tab, text="Add Employee")
            self.__add_emp_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        elif self.__active_tab == "update":  # show update employee submenu
            self.__member_id_label = tk.Label(self.__instructors_tab, text="Employee ID*: ")
            self.__member_id_label.place(relx=0.37, rely=0.2, anchor=tk.CENTER)
            self.__member_id_entry = tk.Entry(self.__instructors_tab)
            self.__member_id_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__name_label = tk.Label(self.__instructors_tab, text="Name: ")
            self.__name_label.place(relx=0.2, rely=0.27, anchor=tk.CENTER)
            self.__name_entry = tk.Entry(self.__instructors_tab)
            self.__name_entry.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
            self.__update_name_button = tk.Button(self.__instructors_tab, text="Update Name")
            self.__update_name_button.place(relx=0.2, rely=0.37, anchor=tk.CENTER)

            self.__phone_label = tk.Label(self.__instructors_tab, text="Phone Number: ")
            self.__phone_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
            self.__phone_entry = tk.Entry(self.__instructors_tab)
            self.__phone_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            self.__update_phone_button = tk.Button(self.__instructors_tab, text="Update Phone Number")
            self.__update_phone_button.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

            self.__email_label = tk.Label(self.__instructors_tab, text="Email Address: ")
            self.__email_label.place(relx=0.8, rely=0.27, anchor=tk.CENTER)
            self.__email_entry = tk.Entry(self.__instructors_tab)
            self.__email_entry.place(relx=0.8, rely=0.3, anchor=tk.CENTER)
            self.__update_email_button = tk.Button(self.__instructors_tab, text="Update Email")
            self.__update_email_button.place(relx=0.8, rely=0.37, anchor=tk.CENTER)
        elif self.__active_tab == "view":  # show view employee submenu
            self.__table = ttk.Treeview(self.__instructors_tab, columns=("Name", "Gender", "Email Address", "Phone No.",  "Manager Name"), show="headings")
            self.__table.place(relx=0.5, rely=0.5, height=400, anchor=tk.CENTER)
        elif self.__active_tab == "delete":  # show delete employee submenu
            self.__emp_id_label = tk.Label(self.__instructors_tab, text="Employee ID*: ")
            self.__emp_id_label.place(relx=0.39, rely=0.2, anchor=tk.CENTER)
            self.__emp_id_entry = tk.Entry(self.__instructors_tab)
            self.__emp_id_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__delete_button = tk.Button(self.__instructors_tab, text="Delete Employee")
            self.__delete_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # show the result text box that holds a message for any action performed by the user
        self.__result_text = tk.Text(self.__instructors_tab, height=1.1, width=30)
        self.__result_text.tag_configure("center", justify="center")

    def hide_emp_tab_labels(self) -> None:
        """
        Hides the active book submenu
        """
        if self.__active_tab == "add":  # hide add book submenu
            self.__name_label.place_forget()
            self.__name_entry.place_forget()
            self.__gender_label.place_forget()
            self.__gender_entry.place_forget()
            self.__phone_label.place_forget()
            self.__phone_entry.place_forget()
            self.__email_label.place_forget()
            self.__email_entry.place_forget()
            self.__manager_id_label.place_forget()
            self.__manager_id_entry.place_forget()
            self.__add_emp_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "update":  # hide update book submenu
            self.__member_id_label.place_forget()
            self.__member_id_entry.place_forget()
            self.__name_label.place_forget()
            self.__name_entry.place_forget()
            self.__update_name_button.place_forget()
            self.__phone_label.place_forget()
            self.__phone_entry.place_forget()
            self.__update_phone_button.place_forget()
            self.__email_label.place_forget()
            self.__email_entry.place_forget()
            self.__update_email_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "view":  # hide view book submenu
            self.__table.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "delete":  # hide delete book submenu
            self.__emp_id_label.place_forget()
            self.__emp_id_entry.place_forget()
            self.__delete_button.place_forget()
            self.__result_text.place_forget()
        
    def show_add_emp_ui(self):
        """
        Initializes the add emp submenu
        """
        def __add_emp():
            """
            Adds a member to the library database
            """
            self.__result_text.insert(tk.END, "", "center")
            
            # get new member info from the gui and create a new member object
            name = self.__name_entry.get()
            gender = self.__gender_entry.get()
            phone = self.__phone_entry.get()
            email = self.__email_entry.get()
            try:
                manager_id = int(self.__manager_id_entry.get())
            except ValueError:
                # display an error message if the manager id is not an integer
                self.__result_text.insert(tk.END, "Manager ID must be an integer", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return

            if not verify_phone_number(phone):  # checks phone number and email formats, sends an error if invalid
                self.__result_text.insert(tk.END, "Invalid Phone Number", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return
            if not verify_email(email):
                self.__result_text.insert(tk.END, "Invalid Email Address", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return

            new_emp = Employee(
                emp_name=name,
                emp_gender=gender,
                emp_email=email,
                emp_phone_no=phone,
                emp_manager_id=manager_id
            )
            
            # execute insert query and display a message based on the result
            if self.__exec.insert_row("Employee", new_emp.model_dump()):
                self.__result_text.insert(tk.END, "Employee Added Successfully", "center")
            else:
                self.__result_text.insert(tk.END, "Failed to Add Employee", "center")
            
            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_emp_tab_labels() # hide any active submenu
        self.show_emp_tab_labels("add") # show the add book submenu
        self.__add_emp_button.config(command=__add_emp) # set the command for the add book button
    
    def show_update_emp_ui(self):
        """
        Initializes the update employee submenu
        """
        def __update_emp(entry: tk.Entry, field_name: str):
            """
            Updates an employee's info in the library database
            :param entry: tk.Entry: The entry widget for the field to update
            :param field_name: str: The field to update
            """
            self.__result_text.insert(tk.END, "", "center")

            if field_name == "emp_phone_no":  # checks phone number and email formats, sends an error if invalid
                if not verify_phone_number(entry.get()):
                    self.__result_text.insert(tk.END, "Invalid Phone Number", "center")
                    self.__result_text.config(state=tk.DISABLED)
                    self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                    return
            elif field_name == "emp_email":
                if not verify_email(entry.get()):
                    self.__result_text.insert(tk.END, "Invalid Email Address", "center")
                    self.__result_text.config(state=tk.DISABLED)
                    self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                    return
                
            # define dict to hold the info needed for the update and send the query
            data = {field_name: f"'{entry.get()}'", "emp_id": f"{self.__member_id_entry.get()}"}
            if self.__exec.update_row("Employee", data):
                self.__result_text.insert(tk.END, "Member Updated Successfully", "center")
            else:
                self.__result_text.insert(tk.END, "Failed to Update Member", "center")
            
            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_emp_tab_labels()
        self.show_emp_tab_labels("update")

        # buttons to update each field separately
        self.__update_name_button.config(command=lambda: __update_emp(self.__name_entry, "emp_name"))
        self.__update_email_button.config(command=lambda: __update_emp(self.__email_entry, "emp_email"))
        self.__update_phone_button.config(command=lambda: __update_emp(self.__phone_entry, "emp_phone_no"))

    def show(self):
        """
        Initializes the view employees submenu
        """
        self.hide_emp_tab_labels()  
        self.show_emp_tab_labels("view")

        # set the headings for the table's columns
        self.__table.heading("Name", text="Name")
        self.__table.heading("Gender", text="Gender")
        self.__table.heading("Email Address", text="Email Address")
        self.__table.heading("Phone No.", text="Phone No.")
        self.__table.heading("Manager Name", text="Manager Name")

        # retrieve all employees from the database and display them in the table
        emps_result = self.__exec.retrieve_all("SimpleEmployees")
        print(emps_result)
        if emps_result and isinstance(emps_result, list):
            for row in emps_result:
                self.__table.insert("", tk.END
                    , values=row)

    def show_delete_emp_ui(self):
        """
        Initializes the delete employee submenu
        """
        def __delete_emp():
            """
            Deletes an employee from the library database
            """
            self.__result_text.insert(tk.END, "", "center")

            try:
                emp_id = int(self.__emp_id_entry.get())  # get the emp id
            except ValueError:
                # display an error message if the emp id is not an integer
                self.__result_text.insert(tk.END, "Employee ID must be an integer", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return
            
            if self.__exec.delete_row("Employee", {"emp_id": emp_id}):  # delete the emp from the database
                self.__result_text.insert(tk.END, "Employee Removed From Database Successfully", "center")
            else:
                # show an error if the deletion failed
                self.__result_text.insert(tk.END, "Failed to Remove Employee", "center")

            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_emp_tab_labels()
        self.show_emp_tab_labels("delete")

        self.__delete_button.config(command=__delete_emp)

    def create_emps_tab(self) -> None:
        """
        Defines the employee management tab menu navigation
        """
        self.__instructors_tab = ttk.Frame(self.__notebook)
        self.__notebook.add(self.__instructors_tab, text="Manage Employees", padding=5)

        # define add, view, update, and delete submenu buttons
        self.__add_client_button = tk.Button(self.__instructors_tab, text="Add Employee", justify=tk.CENTER, command=self.show_add_emp_ui)
        self.__add_client_button.place(relx=0.2, rely=0.05, anchor=tk.CENTER)

        self._view_client_button = tk.Button(self.__instructors_tab, text="View Employees", justify=tk.CENTER, command=self.show)
        self._view_client_button.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
        
        self.__update_client_button = tk.Button(self.__instructors_tab, text="Update Employees", justify=tk.CENTER, command=self.show_update_emp_ui)
        self.__update_client_button.place(relx=0.6, rely=0.05, anchor=tk.CENTER)

        self.__delete_employees_button = tk.Button(self.__instructors_tab, text="Delete Employee", justify=tk.CENTER, command=self.show_delete_emp_ui)
        self.__delete_employees_button.place(relx=0.8, rely=0.05, anchor=tk.CENTER)

class ManageClientsTab:
    def __init__(self, exec: DatabaseExecutor, notebook: ttk.Notebook) -> None:
        self.__exec = exec
        self.__notebook = notebook

        self.__active_tab = ""

    def show_clients_tab_labels(self, menu_to_show: str) -> None:
        """
        Shows the menu for the given client submenu
        :param menu_to_show: str: The submenu to show
        """
        self.__active_tab = menu_to_show
        if self.__active_tab == "add":  # show add client submenu
            self.__name_label = tk.Label(self.__clients_tab, text="Full Name: ")
            self.__name_label.place(relx=0.2, rely=0.125, anchor=tk.CENTER)
            self.__name_entry = tk.Entry(self.__clients_tab)
            self.__name_entry.place(relx=0.4, rely=0.125, anchor=tk.CENTER)

            self.__gender_label = tk.Label(self.__clients_tab, text="Gender: ")
            self.__gender_label.place(relx=0.6, rely=0.125, anchor=tk.CENTER)
            self.__gender_entry = tk.Entry(self.__clients_tab)
            self.__gender_entry.place(relx=0.8, rely=0.125, anchor=tk.CENTER)

            self.__phone_label = tk.Label(self.__clients_tab, text="Phone Number: ")
            self.__phone_label.place(relx=0.2, rely=0.25, anchor=tk.CENTER)
            self.__phone_entry = tk.Entry(self.__clients_tab)
            self.__phone_entry.place(relx=0.4, rely=0.25, anchor=tk.CENTER)

            self.__email_label = tk.Label(self.__clients_tab, text="Email Address: ")
            self.__email_label.place(relx=0.6, rely=0.25, anchor=tk.CENTER)
            self.__email_entry = tk.Entry(self.__clients_tab)
            self.__email_entry.place(relx=0.8, rely=0.25, anchor=tk.CENTER)
           
            self.__client_age_label = tk.Label(self.__clients_tab, text="Client Age: ")
            self.__client_age_label.place(relx=0.2, rely=0.375, anchor=tk.CENTER)
            self.__client_age_entry = tk.Entry(self.__clients_tab)
            self.__client_age_entry.place(relx=0.4, rely=0.375, anchor=tk.CENTER)

            self.__inst_id_label = tk.Label(self.__clients_tab, text="Instructor ID: ")
            self.__inst_id_label.place(relx=0.6, rely=0.375, anchor=tk.CENTER)
            self.__inst_id_entry = tk.Entry(self.__clients_tab)
            self.__inst_id_entry.place(relx=0.8, rely=0.375, anchor=tk.CENTER)

            self.__client_emergency_contact_name_label = tk.Label(self.__clients_tab, text="Emergency Contact Name: ")
            self.__client_emergency_contact_name_label.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
            self.__client_emergency_contact_name_entry = tk.Entry(self.__clients_tab)
            self.__client_emergency_contact_name_entry.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

            self.__client_emergency_contact_phone_label = tk.Label(self.__clients_tab, text="Emergency Contact Phone #: ")
            self.__client_emergency_contact_phone_label.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
            self.__client_emergency_contact_phone_entry = tk.Entry(self.__clients_tab)
            self.__client_emergency_contact_phone_entry.place(relx=0.8, rely=0.5, anchor=tk.CENTER)


            self.__add_client_button = tk.Button(self.__clients_tab, text="Register Client")
            self.__add_client_button.place(relx=0.5, rely=.75, anchor=tk.CENTER)
        elif self.__active_tab == "update":  # show update client submenu
            self.__member_id_label = tk.Label(self.__clients_tab, text="Client ID*: ")
            self.__member_id_label.place(relx=0.37, rely=0.2, anchor=tk.CENTER)
            self.__member_id_entry = tk.Entry(self.__clients_tab)
            self.__member_id_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__name_label = tk.Label(self.__clients_tab, text="Name: ")
            self.__name_label.place(relx=0.2, rely=0.27, anchor=tk.CENTER)
            self.__name_entry = tk.Entry(self.__clients_tab)
            self.__name_entry.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
            self.__update_name_button = tk.Button(self.__clients_tab, text="Update Name")
            self.__update_name_button.place(relx=0.2, rely=0.37, anchor=tk.CENTER)

            self.__phone_label = tk.Label(self.__clients_tab, text="Phone Number: ")
            self.__phone_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
            self.__phone_entry = tk.Entry(self.__clients_tab)
            self.__phone_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            self.__update_phone_button = tk.Button(self.__clients_tab, text="Update Phone Number")
            self.__update_phone_button.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

            self.__email_label = tk.Label(self.__clients_tab, text="Email Address: ")
            self.__email_label.place(relx=0.8, rely=0.27, anchor=tk.CENTER)
            self.__email_entry = tk.Entry(self.__clients_tab)
            self.__email_entry.place(relx=0.8, rely=0.3, anchor=tk.CENTER)
            self.__update_email_button = tk.Button(self.__clients_tab, text="Update Email")
            self.__update_email_button.place(relx=0.8, rely=0.37, anchor=tk.CENTER)
        elif self.__active_tab == "view":  # show view client submenu
            self.__table = ttk.Treeview(self.__clients_tab, columns=("Client Name", "Gender", "Instructor Name", "Registered At"), show="headings")
            self.__table.place(relx=0.5, rely=0.5, height=400, anchor=tk.CENTER)

        # show the result text box that holds a message for any action performed by the user
        self.__result_text = tk.Text(self.__clients_tab, height=1.1, width=30)
        self.__result_text.tag_configure("center", justify="center")

    def hide_clients_tab_labels(self) -> None:
        """
        Hides the active book submenu
        """
        if self.__active_tab == "add":  # hide add book submenu
            self.__name_label.place_forget()
            self.__name_entry.place_forget()
            self.__gender_label.place_forget()
            self.__gender_entry.place_forget()
            self.__phone_label.place_forget()
            self.__phone_entry.place_forget()
            self.__email_label.place_forget()
            self.__email_entry.place_forget()
            self.__client_emergency_contact_name_label.place_forget()
            self.__client_emergency_contact_name_entry.place_forget()
            self.__client_emergency_contact_phone_label.place_forget()
            self.__client_emergency_contact_phone_entry.place_forget()
            self.__client_age_label.place_forget()
            self.__client_age_entry.place_forget()
            self.__add_client_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "update":  # hide update book submenu
            self.__member_id_label.place_forget()
            self.__member_id_entry.place_forget()
            self.__name_label.place_forget()
            self.__name_entry.place_forget()
            self.__update_name_button.place_forget()
            self.__phone_label.place_forget()
            self.__phone_entry.place_forget()
            self.__update_phone_button.place_forget()
            self.__email_label.place_forget()
            self.__email_entry.place_forget()
            self.__update_email_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "view":  # hide view book submenu
            self.__table.place_forget()
            self.__result_text.place_forget()
        
    def show_add_client_ui(self):
        """
        Initializes the add client submenu
        """
        def __add_client():
            """
            Adds a client to the database
            """
            self.__result_text.insert(tk.END, "", "center")
            
            # get new client info from the gui and create a new member object
            name = self.__name_entry.get()
            gender = self.__gender_entry.get()
            phone = self.__phone_entry.get()
            email = self.__email_entry.get()
            client_emergency_contact_name = self.__client_emergency_contact_name_entry.get()
            client_emergency_contact_phone = self.__client_emergency_contact_phone_entry.get()

            try:
                client_age = int(self.__client_age_entry.get())
                inst_id = int(self.__inst_id_entry.get())
            except ValueError:
                # display an error message if the manager id is not an integer
                self.__result_text.insert(tk.END, "Numerical fields cannot contain non-numerical characters", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return

            if not verify_phone_number(phone):  # checks phone number and email formats, sends an error if invalid
                self.__result_text.insert(tk.END, "Invalid Phone Number", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return
            if not verify_email(email):
                self.__result_text.insert(tk.END, "Invalid Email Address", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return

            new_client = Client(
                client_name=name,
                client_gender=gender,
                client_email=email,
                client_phone_no=phone,
                client_inst_id=inst_id,
                client_emergency_contact_name=client_emergency_contact_name,
                client_emergency_contact_phone=client_emergency_contact_phone,
                client_age=client_age
            )
            
            # execute insert query and display a message based on the result
            if self.__exec.insert_row("Client", new_client.model_dump()):
                self.__result_text.insert(tk.END, "Client Added Successfully", "center")
            else:
                self.__result_text.insert(tk.END, "Failed to Add Client", "center")
            
            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_clients_tab_labels() # hide any active submenu
        self.show_clients_tab_labels("add") # show the add book submenu
        self.__add_client_button.config(command=__add_client) # set the command for the add book button
    
    def show_update_client_ui(self):
        """
        Initializes the update client submenu
        """
        def __update_client(entry: tk.Entry, field_name: str):
            """
            Updates an employee's info in the library database
            :param entry: tk.Entry: The entry widget for the field to update
            :param field_name: str: The field to update
            """
            self.__result_text.insert(tk.END, "", "center")

            if field_name == "emp_phone_no":  # checks phone number and email formats, sends an error if invalid
                if not verify_phone_number(entry.get()):
                    self.__result_text.insert(tk.END, "Invalid Phone Number", "center")
                    self.__result_text.config(state=tk.DISABLED)
                    self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                    return
            elif field_name == "emp_email":
                if not verify_email(entry.get()):
                    self.__result_text.insert(tk.END, "Invalid Email Address", "center")
                    self.__result_text.config(state=tk.DISABLED)
                    self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                    return
                
            # define dict to hold the info needed for the update and send the query
            data = {field_name: f"'{entry.get()}'", "emp_id": f"{self.__member_id_entry.get()}"}
            if self.__exec.update_row("Client", data):
                self.__result_text.insert(tk.END, "Client Updated Successfully", "center")
            else:
                self.__result_text.insert(tk.END, "Failed to Update Client", "center")
            
            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_clients_tab_labels()
        self.show_clients_tab_labels("update")

        # buttons to update each field separately
        self.__update_name_button.config(command=lambda: __update_client(self.__name_entry, "emp_name"))
        self.__update_email_button.config(command=lambda: __update_client(self.__email_entry, "emp_email"))
        self.__update_phone_button.config(command=lambda: __update_client(self.__phone_entry, "emp_phone_no"))

    def show(self):
        """
        Initializes the view employees submenu
        """
        self.hide_clients_tab_labels()  
        self.show_clients_tab_labels("view")

        # set the headings for the table's columns
        self.__table.heading("Client Name", text="Client Name")
        self.__table.heading("Gender", text="Gender")
        self.__table.heading("Instructor Name", text="Instructor Name")
        self.__table.heading("Registered At", text="Registered At")

        # retrieve all employees from the database and display them in the table
        emps_result = self.__exec.retrieve_all("SimpleClients")
        print(emps_result)
        if emps_result and isinstance(emps_result, list):
            for row in emps_result:
                self.__table.insert("", tk.END
                    , values=row)

    def create_clients_tab(self) -> None:
        """
        Defines the employee management tab menu navigation
        """
        self.__clients_tab = ttk.Frame(self.__notebook)
        self.__notebook.add(self.__clients_tab, text="Manage Clients", padding=5)

        # define add, view, update, and delete submenu buttons
        self.__add_client_button = tk.Button(self.__clients_tab, text="Register New Client", justify=tk.CENTER, command=self.show_add_client_ui)
        self.__add_client_button.place(relx=0.2, rely=0.05, anchor=tk.CENTER)

        self._view_client_button = tk.Button(self.__clients_tab, text="View Clients", justify=tk.CENTER, command=self.show)
        self._view_client_button.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
        
        self.__update_client_button = tk.Button(self.__clients_tab, text="Update Client", justify=tk.CENTER, command=self.show_update_client_ui)
        self.__update_client_button.place(relx=0.6, rely=0.05, anchor=tk.CENTER)

class ManageVehiclesTab:
    def __init__(self, exec: DatabaseExecutor, notebook: ttk.Notebook) -> None:
        self.__exec = exec
        self.__notebook = notebook

        self.__active_menu = ""

    def show_vehicle_tab_labels(self, menu_to_show: str) -> None:
        """
        Shows the menu for the given vehicles submenu
        :param menu_to_show: str: The submenu to show
        """
        self.__active_menu = menu_to_show
        if self.__active_menu == "add":  # show add vehicle submenu
            self.__vehicle_license_no_label = tk.Label(self.__vehicles_tab, text="License Plate No*: ")
            self.__vehicle_license_no_label.place(relx=0.39, rely=0.2, anchor=tk.CENTER)
            self.__vehicle_license_no_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_license_no_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__vehicle_make_label = tk.Label(self.__vehicles_tab, text="Vehicle Make: ")
            self.__vehicle_make_label.place(relx=0.39, rely=0.3, anchor=tk.CENTER)
            self.__vehicle_make_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_make_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

            self.__vehicle_model_label = tk.Label(self.__vehicles_tab, text="Vehicle Model: ")
            self.__vehicle_model_label.place(relx=0.39, rely=0.25, anchor=tk.CENTER)
            self.__vehicle_model_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_model_entry.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

            self.__vehicle_year_label = tk.Label(self.__vehicles_tab, text="Vehicle Year: ")
            self.__vehicle_year_label.place(relx=0.39, rely=0.35, anchor=tk.CENTER)
            self.__vehicle_year_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_year_entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

            self.__vehicle_color_label = tk.Label(self.__vehicles_tab, text="Vehicle Color: ")
            self.__vehicle_color_label.place(relx=0.39, rely=0.4, anchor=tk.CENTER)
            self.__vehicle_color_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_color_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

            self.__vehicle_inspection_date_label = tk.Label(self.__vehicles_tab, text="Last Inspected On: ")
            self.__vehicle_inspection_date_label.place(relx=0.39, rely=0.3, anchor=tk.CENTER)
            self.__vehicle_inspection_date_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_inspection_date_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

            self.__add_vehicle_button = tk.Button(self.__vehicles_tab, text="Add Book")
            self.__add_vehicle_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        elif self.__active_menu == "update":  # show update vehicle submenu
            self.__vehicle_license_no_label = tk.Label(self.__vehicles_tab, text="License Plate No*: ")
            self.__vehicle_license_no_label.place(relx=0.39, rely=0.2, anchor=tk.CENTER)
            self.__vehicle_license_no_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_license_no_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__vehicle_inspection_date_label = tk.Label(self.__vehicles_tab, text="Last Inspected On: ")
            self.__vehicle_inspection_date_label.place(relx=0.39, rely=0.3, anchor=tk.CENTER)
            self.__vehicle_inspection_date_entry = tk.Entry(self.__vehicles_tab)
            self.__vehicle_inspection_date_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

            self.__update_date_button = tk.Button(self.__vehicles_tab, text="Make Available")
            self.__update_date_button.place(relx=0.4, rely=0.3, anchor=tk.CENTER)

        elif self.__active_menu == "view":  # show view vehicle submenu
            self.__table = ttk.Treeview(self.__vehicles_tab, columns=("License Plate", "Make", "Model", "Year", "Color", "Last Inspected On"), show="headings")
            self.__table.place(relx=0.5, rely=0.5, height=400, anchor=tk.CENTER)

        # show the result text box that holds a message for any action performed by the user
        self.__result_text = tk.Text(self.__vehicles_tab, height=1.1, width=30)
        self.__result_text.tag_configure("center", justify="center")

    def hide_vehicle_tab_labels(self) -> None:
        """
        Hides the active book submenu
        """
        if self.__active_menu == "add":  # hide add book submenu
            self.__vehicle_license_no_label.place_forget()
            self.__vehicle_license_no_entry.place_forget()
            self.__vehicle_make_label.place_forget()
            self.__vehicle_make_entry.place_forget()
            self.__vehicle_model_label.place_forget()
            self.__vehicle_model_entry.place_forget()
            self.__vehicle_year_label.place_forget()
            self.__vehicle_year_entry.place_forget()
            self.__vehicle_color_label.place_forget()
            self.__vehicle_color_entry.place_forget()
            self.__vehicle_inspection_date_label.place_forget()
            self.__vehicle_inspection_date_entry.place_forget()
            self.__add_vehicle_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_menu == "update":  # hide update book submenu
            self.__vehicle_license_no_label.place_forget()
            self.__vehicle_license_no_entry.place_forget()
            self.__vehicle_inspection_date_label.place_forget()
            self.__vehicle_inspection_date_entry.place_forget()
            self.__update_date_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_menu == "view":  # hide view book submenu
            self.__table.place_forget()
            self.__result_text.place_forget()
        
    def show_add_vehicle_ui(self):
        """
        Initializes the add book submenu
        """
        def __add_book():
            """
            Adds a book to the library database
            """
            self.__result_text.insert(tk.END, "", "center")  # clear the result text box

            license_no = self.__vehicle_license_no_entry.get()
            make = self.__vehicle_make_entry.get()
            model = self.__vehicle_model_entry.get()
            year = self.__vehicle_year_entry.get()
            color = self.__vehicle_color_entry.get()
            last_inspection = self.__vehicle_inspection_date_entry.get()

            new_vehicle = Vehicle(
                vehicle_license_no=license_no,
                vehicle_make=make,
                vehicle_model=model,
                vehicle_year=year,
                vehicle_color=color,
                vehicle_last_inspection=last_inspection
            )
            
            # insert the book into the database, and display a message to the user based on the result
            if self.__exec.insert_row("Vehicle", new_vehicle.model_dump()):  
                self.__result_text.insert(tk.END, "Vehicle Added Successfully", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
            else:
                self.__result_text.insert(tk.END, "Failed to Add Vehicle", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_vehicle_tab_labels() # hide any active submenu
        self.show_vehicle_tab_labels("add") # show the add book submenu
        self.__add_vehicle_button.config(command=__add_book) # set the command for the add book button
    
    def show_update_vehicle_ui(self):
        """
        Initializes the update vehicle submenu
        """
        def __update_book():
            """
            Updates a vehicle's last inspected date in the database
            """
            self.__result_text.insert(tk.END, "", "center")  # clear the result text box

            data = {"vehicle_last_inspection": f"'{self.__vehicle_inspection_date_entry.get()}'", "vehicle_license_no": f"'{self.__vehicle_license_no_entry.get()}'"}
            if self.__exec.update_row("Vehicle", data):  # update the book in the database
                self.__result_text.insert(tk.END, "Vehicle Updated Successfully", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
            else:
                self.__result_text.insert(tk.END, "Failed to Update Vehicle", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_vehicle_tab_labels()
        self.show_vehicle_tab_labels("update")

        self.__update_date_button.config(command=__update_book)
        self.__update_date_button.place(relx=0.4, rely=0.3, anchor=tk.CENTER)

    def show_view_vehicles_ui(self):
        """
        Initializes the view books submenu
        """
        self.hide_vehicle_tab_labels()  
        self.show_vehicle_tab_labels("view")

        # set the headings for the table's columns
        self.__table.heading("License Plate", text="License Plate")
        self.__table.heading("Make", text="Make")
        self.__table.heading("Model", text="Model")
        self.__table.heading("Year", text="Year")
        self.__table.heading("Color", text="Color")
        self.__table.heading("Last Inspected On", text="Last Inspected On")

        # retrieve all books from the database and display them in the table
        books_result = self.__exec.retrieve_all("Vehicle")
        print(books_result)
        if books_result and isinstance(books_result, list):
            for row in books_result:
                self.__table.insert("", tk.END
                    , values=row)

    def create_vehicles_tab(self) -> None:
        """
        Defines the vehicles tab menu navigation
        """
        self.__vehicles_tab = ttk.Frame(self.__notebook)
        self.__notebook.add(self.__vehicles_tab, text="Manage Vehicles", padding=5)

        # define add, view, update, and delete submenu buttons
        self.__add_vehicle_button = tk.Button(self.__vehicles_tab, text="Add Vehicle", justify=tk.CENTER, command=self.show_add_vehicle_ui)
        self.__add_vehicle_button.place(relx=0.2, rely=0.05, anchor=tk.CENTER)

        self.__view_vehicles_button = tk.Button(self.__vehicles_tab, text="View Vehicles", justify=tk.CENTER, command=self.show_view_vehicles_ui)
        self.__view_vehicles_button.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
        
        self.__update_vehicle_button = tk.Button(self.__vehicles_tab, text="Update Vehicle", justify=tk.CENTER, command=self.show_update_vehicle_ui)
        self.__update_vehicle_button.place(relx=0.6, rely=0.05, anchor=tk.CENTER)

def main():
    app = SDCApp("Smooth Driving College of Motoring Portal", 1200, 800)
    app.mainloop()

if __name__ == "__main__":
    main()

