import tkinter as tk
from tkinter import ttk

from backend.load.executor import DatabaseExecutor
from backend.data.sdc_data import (
    Meeting,
    MeetingType,
    Interview
)
from validators import (
    verify_time,
    verify_date,
    verify_datetime
)

class InstructorPortal:
    def __init__(self, exec: DatabaseExecutor, notebook: ttk.Notebook) -> None:
        self.__exec = exec
        self.__notebook = notebook

        self.__manage_inst_tab = ManageSessionsTab(self.__exec, self.__notebook)
        
        self.__manage_inst_tab.create_sessions_tab()

        self.__notebook.pack()

class ManageSessionsTab:
    def __init__(self, exec: DatabaseExecutor, notebook: ttk.Notebook) -> None:
        self.__exec = exec
        self.__notebook = notebook

        self.__active_tab = ""

    def show_session_tab_labels(self, menu_to_show: str) -> None:
        """
        Shows the menu for the give meeting submenu
        :param menu_to_show: str: The submenu to show
        """
        self.__active_tab = menu_to_show
        self.__handle_session_type_change()
        if self.__active_tab == "add":  # show add meeting submenu
            self.__add_session_button = tk.Button(self.__sessions_tab, text="Schedule Session")
            self.__add_session_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        elif self.__active_tab == "view":  # show view meeting submenu
            self.__view_meeting_button = tk.Button(self.__sessions_tab, text="Find Sessions")
            self.__view_meeting_button.place(relx=0.7, rely=0.2, anchor=tk.CENTER)
        elif self.__active_tab == "delete":  # show delete meeting submenu
            self.__client_id_label = tk.Label(self.__sessions_tab, text="Client ID*: ")
            self.__client_id_label.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
            self.__client_id_entry = tk.Entry(self.__sessions_tab)
            self.__client_id_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__inst_id_label = tk.Label(self.__sessions_tab, text="Instructor ID*: ")
            self.__inst_id_label.place(relx=0.35, rely=0.3, anchor=tk.CENTER)
            self.__inst_id_entry = tk.Entry(self.__sessions_tab)
            self.__inst_id_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

            self.__meeting_start_label = tk.Label(self.__sessions_tab, text="Meeting Start Time*: ")
            self.__meeting_start_label.place(relx=0.35, rely=0.4, anchor=tk.CENTER)
            self.__meeting_start_entry = tk.Entry(self.__sessions_tab)
            self.__meeting_start_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

            self.__delete_button = tk.Button(self.__sessions_tab, text="Delete Session")
            self.__delete_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # show the result text box that holds a message for any action performed by the user
        self.__result_text = tk.Text(self.__sessions_tab, height=1.1, width=30)
        self.__result_text.tag_configure("center", justify="center")
    
    # Add this helper method to dynamically update fields
    def __update_fields_based_on_session_type(self, event=None):
        """
        Updates the fields shown in the UI based on the selected session type.
        """
        self.__clear_dynamic_fields()
        self.__session_type = self.__session_type_var.get()
        if self.__active_tab == "add":
            self.__client_id_label = tk.Label(self.__sessions_tab, text="Client ID: ")
            self.__client_id_label.place(relx=0.2, rely=0.2, anchor=tk.CENTER)
            self.__client_id_entry = tk.Entry(self.__sessions_tab)
            self.__client_id_entry.place(relx=0.4, rely=0.2, anchor=tk.CENTER)

            self.__inst_id_label = tk.Label(self.__sessions_tab, text="Instructor ID: ")
            self.__inst_id_label.place(relx=0.6, rely=0.2, anchor=tk.CENTER)
            self.__inst_id_entry = tk.Entry(self.__sessions_tab)
            self.__inst_id_entry.place(relx=0.8, rely=0.2, anchor=tk.CENTER)

            self.__location_label = tk.Label(self.__sessions_tab, text="Location: ")
            self.__location_label.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
            self.__location_entry = tk.Entry(self.__sessions_tab)
            self.__location_entry.place(relx=0.4, rely=0.3, anchor=tk.CENTER)

            self.__location_id_label = tk.Label(self.__sessions_tab, text="Location ID: ")
            self.__location_id_label.place(relx=0.6, rely=0.3, anchor=tk.CENTER)
            self.__location_id_entry = tk.Entry(self.__sessions_tab)
            self.__location_id_entry.place(relx=0.8, rely=0.3, anchor=tk.CENTER)

            self.__session_date_label = tk.Label(self.__sessions_tab, text="Session Date: ")
            self.__session_date_label.place(relx=0.2, rely=0.4, anchor=tk.CENTER)
            self.__session_date_entry = tk.Entry(self.__sessions_tab)
            self.__session_date_entry.place(relx=0.4, rely=0.4, anchor=tk.CENTER)
            
            self.__start_label = tk.Label(self.__sessions_tab, text="Start Time: ")
            self.__start_label.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
            self.__start_entry = tk.Entry(self.__sessions_tab)
            self.__start_entry.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

            if self.__session_type == "Lesson/Exam":
                self.__vehicle_license_label = tk.Label(self.__sessions_tab, text="Vehicle License No: ")
                self.__vehicle_license_label.place(relx=0.6, rely=0.4, anchor=tk.CENTER)
                self.__vehicle_license_entry = tk.Entry(self.__sessions_tab)
                self.__vehicle_license_entry.place(relx=0.8, rely=0.4, anchor=tk.CENTER)

                self.__end_label = tk.Label(self.__sessions_tab, text="End Time: ")
                self.__end_label.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
                self.__end_entry = tk.Entry(self.__sessions_tab)
                self.__end_entry.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

                self.__type_label = tk.Label(self.__sessions_tab, text="Type: ")
                self.__type_label.place(relx=0.4, rely=0.6, anchor=tk.CENTER)
                self.__type_var = tk.StringVar()
                self.__type_dropdown = ttk.Combobox(
                    self.__sessions_tab,
                    textvariable=self.__type_var,
                    values=["LESSON", "WRITTEN EXAM", "DRIVING EXAM"],
                    state="readonly"
                )
                self.__type_dropdown.place(relx=0.6, rely=0.6, anchor=tk.CENTER)
        elif self.__active_tab == "view":
            self.__inst_id_label = tk.Label(self.__sessions_tab, text="Instructor ID: ")
            self.__inst_id_label.place(relx=0.37, rely=0.2, anchor=tk.CENTER)
            self.__inst_id_entry = tk.Entry(self.__sessions_tab)
            self.__inst_id_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
            if self.__session_type == "Lesson/Exam":
                self.__table = ttk.Treeview(self.__sessions_tab, columns=("Client", "Instructor", "Start", "End", "Type"), show="headings")
                self.__table.place(relx=0.5, rely=0.5, height=400, anchor=tk.CENTER)
            elif self.__session_type == "Interview":
                self.__table = ttk.Treeview(self.__sessions_tab, columns=("Client", "Instructor", "Date"), show="headings")
                self.__table.place(relx=0.5, rely=0.5, height=400, anchor=tk.CENTER)
        elif self.__active_tab == "delete":
            self.__client_id_label = tk.Label(self.__sessions_tab, text="Client ID*: ")
            self.__client_id_label.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
            self.__client_id_entry = tk.Entry(self.__sessions_tab)
            self.__client_id_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            self.__inst_id_label = tk.Label(self.__sessions_tab, text="Instructor ID*: ")
            self.__inst_id_label.place(relx=0.35, rely=0.3, anchor=tk.CENTER)
            self.__inst_id_entry = tk.Entry(self.__sessions_tab)
            self.__inst_id_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

            self.__meeting_start_label = tk.Label(self.__sessions_tab, text="Meeting Start Time*: ")
            self.__meeting_start_label.place(relx=0.35, rely=0.4, anchor=tk.CENTER)
            self.__meeting_start_entry = tk.Entry(self.__sessions_tab)
            self.__meeting_start_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            
    def __clear_dynamic_fields(self):
        """
        Clears all dynamically created fields from the UI.
        """
        for widget in self.__sessions_tab.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry, ttk.Combobox, ttk.Treeview)) and widget not in [self.__session_type_label, self.__session_type_dropdown]:
                widget.place_forget()

    def hide_session_tab_labels(self) -> None:
        """
        Hides the active meeting submenu
        """
        if self.__active_tab == "add":  # hide add meeting submenu
            if self.__session_type == "Lesson/Exam":
                self.__vehicle_license_label.place_forget()
                self.__vehicle_license_entry.place_forget()
                self.__end_label.place_forget()
                self.__end_entry.place_forget()
                self.__type_label.place_forget()
                self.__type_dropdown.place_forget()
            self.__inst_id_label.place_forget()
            self.__inst_id_entry.place_forget()
            self.__inst_id_label.place_forget()
            self.__inst_id_entry.place_forget()
            self.__location_id_label.place_forget()
            self.__location_id_entry.place_forget()
            self.__location_label.place_forget()
            self.__location_entry.place_forget()
            self.__start_label.place_forget()
            self.__start_entry.place_forget()
            self.__session_type_label.place_forget()
            self.__session_type_dropdown.place_forget()
            self.__client_id_label.place_forget()
            self.__client_id_entry.place_forget()
            self.__session_date_label.place_forget()
            self.__session_date_entry.place_forget()
            self.__add_session_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "view":  # hide view meeting submenu
            if self.__session_type:
                self.__table.place_forget()
            self.__inst_id_label.place_forget()
            self.__inst_id_entry.place_forget()
            self.__view_meeting_button.place_forget()
            self.__result_text.place_forget()
        elif self.__active_tab == "delete":  # hide delete meeting submenu
            self.__inst_id_label.place_forget()
            self.__inst_id_entry.place_forget()
            self.__delete_button.place_forget()
            self.__meeting_start_label.place_forget()
            self.__meeting_start_entry.place_forget()
            self.__client_id_label.place_forget()
            self.__client_id_entry.place_forget()
            self.__result_text.place_forget()
        
    def show_add_meeting_ui(self):
        """
        Initializes the add emp submenu
        """
        def __schedule_session():
            """
            Adds a member to the library database
            """
            self.__result_text.insert(tk.END, "", "center")
            
            # get new member info from the gui and create a new member object
            location = self.__location_entry.get()
            date = self.__session_date_entry.get()
            start = self.__start_entry.get()
            
            try:
                client_id = int(self.__client_id_entry.get())
                inst_id = int(self.__inst_id_entry.get())
                location_id = int(self.__location_id_entry.get())
            except ValueError:
                # display an error message if the manager id is not an integer
                self.__result_text.insert(tk.END, "ID must be an integer", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return
            
            if not verify_date(date):  
                self.__result_text.insert(tk.END, "Invalid Date", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return
            if not verify_time(start):
                self.__result_text.insert(tk.END, "Invalid Start Time", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return
            
            if self.__session_type == "Lesson/Exam":
                end = self.__end_entry.get()
                vehicle_license = self.__vehicle_license_entry.get()
                try:
                    meeting_type = MeetingType(self.__type_var.get())
                except ValueError:
                    # display an error message if the meeting type is not valid
                    self.__result_text.insert(tk.END, "Invalid Meeting Type", "center")
                    self.__result_text.config(state=tk.DISABLED)
                    self.__result_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return
                
                if not verify_time(end):
                    self.__result_text.insert(tk.END, "Invalid End Time", "center")
                    self.__result_text.config(state=tk.DISABLED)
                    self.__result_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return
                
                new_session = Meeting(
                    meeting_client_id=client_id,
                    meeting_inst_id=inst_id,
                    meeting_vehicle_no=vehicle_license,
                    meeting_location=location,
                    meeting_location_id=location_id,
                    meeting_start=f"{date} {start}",
                    meeting_end=f"{date} {end}",
                    meeting_type=meeting_type.name
                )

                # execute insert query and display a message based on the result
                if self.__exec.insert_row("Meeting", new_session.model_dump()):
                    self.__result_text.insert(tk.END, "Meeting Scheduled Successfully", "center")
                else:
                    self.__result_text.insert(tk.END, "Failed to Schedule Meeting", "center")

                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                
                return
                
            new_session = Interview(
                interv_client_id=client_id,
                interv_inst_id=inst_id,
                interv_location_id=location_id,
                interv_location=location,
                interv_date=f"{date} {start}"
            )

            # execute insert query and display a message based on the result
            if self.__exec.insert_row("Interview", new_session.model_dump()):
                self.__result_text.insert(tk.END, "Interview Scheduled Successfully", "center")
            else:
                self.__result_text.insert(tk.END, "Failed to Schedule Interview", "center")

            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_session_tab_labels() # hide any active submenu
        self.show_session_tab_labels("add") # show the add book submenu
        self.__add_session_button.config(command=__schedule_session) # set the command for the add book button

    def show(self):
        """
        Initializes the view employees submenu
        """
        def __view_sessions():
            for item in self.__table.get_children():
                self.__table.delete(item)

            try:
                inst_id = int(self.__inst_id_entry.get())
            except ValueError:
                # display an error message if the id is not an integer
                self.__result_text.insert(tk.END, "Instructor ID must be an integer", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return
            
            if self.__session_type == "Lesson/Exam":
                self.__exec.execute_query(f"CALL getInstructorMeetings({inst_id})")  
                meetings_result = self.__exec.retrieve_all("instructorMeetings")  # retrieve all meetings from the database
                self.__table.heading("Client", text="Client")
                self.__table.heading("Instructor", text="Instructor")
                self.__table.heading("Start", text="Start")
                self.__table.heading("End", text="End")
                self.__table.heading("Type", text="Type")
            else:
                self.__exec.execute_query(f"CALL getInstructorInterviews({inst_id})")
                meetings_result = self.__exec.retrieve_all("instructorInterviews")  # retrieve all meetings from the database
                self.__table.heading("Client", text="Client")
                self.__table.heading("Instructor", text="Instructor")
                self.__table.heading("Date", text="Date")
            
            # retrieve all employees from the database and display them in the table
            if meetings_result and isinstance(meetings_result, list):
                for row in meetings_result:
                    self.__table.insert("", tk.END
                        , values=row)
                    
        self.hide_session_tab_labels()  
        self.show_session_tab_labels("view")

        self.__view_meeting_button.config(command=__view_sessions)  # set the command for the view meeting button

    def show_delete_session_ui(self):
        """
        Initializes the delete employee submenu
        """
        def __delete_session():
            """
            Deletes an employee from the library database
            """
            self.__result_text.insert(tk.END, "", "center")

            try:
                client_id = int(self.__client_id_entry.get())  # get the ids from the gui and int cast
                inst_id = int(self.__inst_id_entry.get()) 
            except ValueError:
                # display an error message if an id is not an integer
                self.__result_text.insert(tk.END, "IDs must be integers", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return
            
            session_start = self.__meeting_start_entry.get()
            if not verify_datetime(session_start):
                # display an error message if the datetime is not valid
                self.__result_text.insert(tk.END, "Session Start Time must be a valid datetime value", "center")
                self.__result_text.config(state=tk.DISABLED)
                self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return
            
            if self.__session_type == "Lesson/Exam":
                if self.__exec.delete_row("Meeting", {"meeting_client_id": client_id, "meeting_inst_id": inst_id, "meeting_start": session_start}):  # delete the emp from the database
                    self.__result_text.insert(tk.END, "Meeting Deleted Successfully", "center")
                else:
                    # show an error if the deletion failed
                    self.__result_text.insert(tk.END, "Failed to Delete Meeting", "center")
            else:
                if self.__exec.delete_row("Interview", {"interv_client_id": client_id, "interv_inst_id": inst_id, "interv_date": session_start}):  # delete the emp from the database
                    self.__result_text.insert(tk.END, "Interview Deleted Successfully", "center")
                else:
                    # show an error if the deletion failed
                    self.__result_text.insert(tk.END, "Failed to Delete Interview", "center")

            self.__result_text.config(state=tk.DISABLED)
            self.__result_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.hide_session_tab_labels()
        self.show_session_tab_labels("delete")

        self.__delete_button.config(command=__delete_session)

    def create_sessions_tab(self) -> None:
        """
        Defines the session management tab menu navigation
        """
        self.__sessions_tab = ttk.Frame(self.__notebook)
        self.__notebook.add(self.__sessions_tab, text="Manage Client Sessions", padding=5)

        # define add, view, update, and delete submenu buttons
        self.__add_meeting_button = tk.Button(self.__sessions_tab, text="Schedule Session", justify=tk.CENTER, command=self.show_add_meeting_ui)
        self.__add_meeting_button.place(relx=0.3, rely=0.05, anchor=tk.CENTER)

        self.__view_meeting_button = tk.Button(self.__sessions_tab, text="View Sessions", justify=tk.CENTER, command=self.show)
        self.__view_meeting_button.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.__delete_meeting_button = tk.Button(self.__sessions_tab, text="Delete Session", justify=tk.CENTER, command=self.show_delete_session_ui)
        self.__delete_meeting_button.place(relx=0.7, rely=0.05, anchor=tk.CENTER)

    def __handle_session_type_change(self):
        """
        Handles updates made to the session type dropdown menu. 
        Updates field visibility based on the type selected.
        """
        self.__session_type_label = tk.Label(self.__sessions_tab, text="Session Type: ")
        self.__session_type_label.place(relx=0.3, rely=0.125, anchor=tk.CENTER)
        self.__session_type_var = tk.StringVar()
        self.__session_type_dropdown = ttk.Combobox(
            self.__sessions_tab,
            textvariable=self.__session_type_var,
            values=["Interview", "Lesson/Exam"],
            state="readonly"
        )
        self.__session_type_dropdown.place(relx=0.5, rely=0.125, anchor=tk.CENTER)
        self.__session_type_dropdown.bind("<<ComboboxSelected>>", self.__update_fields_based_on_session_type)
        self.__update_fields_based_on_session_type()
