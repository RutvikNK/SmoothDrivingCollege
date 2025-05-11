from backend.load.connector import SQLConnector
from backend.load.commands import InsertCommand, SelectCommand, DeleteCommand, UpdateCommand

class DatabaseExecutor:
    """
    Handles executing basic queries on the D2 stats database. 
    """
    def __init__(self, db: SQLConnector) -> None:
        self.__db = db
        self.__insert_command: InsertCommand = InsertCommand(db)
        self.__select_command: SelectCommand = SelectCommand(db)
        self.__delete_command: DeleteCommand = DeleteCommand(db)
        self.__update_command: UpdateCommand = UpdateCommand(db)

    def insert_row(self, table_name: str, data: dict):
        """
        Insert row(s) into a table
        """
        self.__insert_command.set_command(table_name, data)
        return self.__insert_command.execute()

    def select_rows(self, table_name: str, fields: list[str], condition: dict):
        """
        Retrieve rows or sepcfifc columns of a row from a table
        """
        self.__select_command.set_command(table_name, fields, condition)
        return self.__select_command.execute()
    
    def update_row(self, table_name: str, data: dict):
        """
        Update rows in a table
        """
        self.__update_command.set_command(table_name, data)
        return self.__update_command.execute()

    def delete_row(self, table_name: str, data: dict):
        """
        Delete rows from a table
        """
        self.__delete_command.set_command(table_name, data)
        return self.__delete_command.execute()
    
    def call_proc(self, proc_name: str, params: list):
        return self.__db.call_proc(proc_name, params)

    def retrieve_all(self, table_name: str):
        return self.__db.retrieve_all(table_name)
    