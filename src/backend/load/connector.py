from mysql import connector


class SQLConnector:
    """
    Utility class that creates a MySQL database connection. Allows for executing queries, as well as commits and rollbacks
    """
    def __init__(self, db_name: str, port: int, user: str="root", password: str="pass", host: str="localhost",) -> None:
        self.db = connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port = port
        )


    def execute(self, query: str, params=None):
        cursor = self.db.cursor(buffered=True)

        if params is None:
            params = []

        try:
            cursor.execute(query, params)

            if query.startswith("SELECT"):
                result = cursor.fetchall()
                if result:
                    return result
                else:
                    return False

            print(query)
            print("Query executed successfully\n")
            self.commit()
            cursor.close()
            return True
        except Exception as e:
            self.rollback()
            print(f"{e}")
            print("Query execution failed\n")
            cursor.close()
            return False

    def call_proc(self, proc_name: str, params: list):
        cursor = self.db.cursor(buffered=True)
        try:
            result = cursor.callproc(proc_name, params)
            print("Procedure call successful\n")
            self.commit()
            cursor.close()
            return result
        except Exception as e:
            self.rollback()
            print(f"{e}")
            print("Procedure call failed\n")
            cursor.close()
            return False

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def close(self) -> None:
        """
        Closes the database connection
        """
        self.db.close()

    def retrieve_all(self, table_name: str):
        """
        Debug function to view all tuples in a table
        """
        result = self.execute(f"SELECT * FROM {table_name}")

        if result:
            return result
