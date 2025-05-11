from abc import ABC, abstractmethod

from backend.connector import SQLConnector


class Command(ABC):
    """
    Command interface
    """
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def set_command(self):
        pass

class InsertCommand(Command):
    """
    Insert command, handles adding rows to the given table. Allows for multiple rows to be added
    """
    def __init__(self, obj: SQLConnector, table_name: str="", data: list[dict]=[{}]) -> None:
        self.__obj = obj
        self.__data = data
        self.__table_name = table_name

    def execute(self):
        """
        Executes an insert query based on the class' attributes.
        """
        query = f"INSERT INTO {self.__table_name}("  # construct base query by populating the column names
        for k in self.__data[0].keys():
            query += f"{k}, "

        query = f"{query[:-2]}) VALUES"

        for value in self.__data:  # populate the query with all rows in the data list
            query += "("
            for attr in value.values():
                if isinstance(attr, float) or isinstance(attr, int):
                    query += f"{attr}, "
                else:
                    query += f'"{attr}", '
            else:
                query = f"{query[:-2]}), "
        else:
            query = f"{query[:-2]}"
        
        print(query)  # print to debug
        result = self.__obj.execute(query)  # execute
        if isinstance(result, bool):
            return result

    def set_command(self, table_name: str, data) -> None:
        """
        Allows setting the command attributes: table name and insertion data
        """
        # query details
        self.__table_name = table_name
        self.__data = [data]  # add empty dictionary for new row

class SelectCommand(Command):
    """
    Select command, handles retrieving specific columns or entire rows from the given table.
    """
    def __init__(self, obj: SQLConnector, table_name: str="", fields: list[str]=[]) -> None:
        self.__obj = obj
        self.__table_name = table_name
        self.__fields = fields
        self.__conditions = dict()
    
    def execute(self):
        """
        Executes the select query based on the given class' attributes
        """
        query = "SELECT "
        if self.__fields:
            for field in self.__fields:
                query += f"{field}, "
            else:
                query = f"{query[:-2]} FROM {self.__table_name}"
        else:
            query += f"* FROM {self.__table_name}"

        if self.__conditions:
            query += " WHERE "
            for k, v, in self.__conditions.items():
                if isinstance(v, int) or isinstance(v, float):
                    query += f"{k} = {v}"
                else:
                    query += f'{k} = "{v}"'

        print(query)
        result = self.__obj.execute(query)
        return result

    def set_command(self, table_name: str, fields: list[str], condition: dict) -> None:
        """
        Allows setting the attributes for the select command
        """
        self.__table_name = table_name
        self.__fields = fields
        self.__conditions = condition

class DeleteCommand(Command):
    """
    Delete command, handles deleting specified rows from the given table.
    """
    def __init__(self, obj: SQLConnector, table_name: str="", data: dict={}) -> None:
        self.__obj = obj
        self.__table_name = table_name
        self.__data = data

    def execute(self):
        """
        Executes the delete command based on the class' attributes
        """
        keys = list(self.__data.keys())
        query = f"DELETE FROM {self.__table_name} WHERE {keys[0]} = "

        if isinstance(self.__data[keys[0]], int) or isinstance(self.__data[keys[0]], float):
            query += f"{self.__data[keys[0]]}"
        else:
            query += f"'{self.__data[keys[0]]}'"

        print(query)
        return self.__obj.execute(query)

    def set_command(self, table_name: str, data: dict) -> None:
        """
        Allows ssetting the attribtues of the delete command
        """
        self.__table_name = table_name
        self.__data = data

class UpdateCommand(Command):
    """
    Update command, handles updating rows in the given table.
    """
    def __init__(self, obj: SQLConnector, table_name: str="", data: dict={}) -> None:
        self.__obj = obj
        self.__table_name = table_name
        self.__data = data

    def execute(self):
        """
        Executes the update query based on the given class' attributes
        """
        keys = list(self.__data.keys())  # get the keys from the dictionary, assuming first key is column to update and second key is condtional column
        query = f"UPDATE {self.__table_name} SET {keys[0]} = {self.__data[keys[0]]} WHERE {keys[1]} = {self.__data[keys[1]]}"

        print(query)
        return self.__obj.execute(query)

    def set_command(self, table_name: str, data: dict) -> None:
        """
        Allows setting the attributes for the update command
        """
        self.__data = data
        self.__table_name = table_name