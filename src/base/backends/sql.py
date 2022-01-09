import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from base.log import Logger
import typing
import os
import subprocess


def check_mysql_installed() -> bool:
    log = Logger("sql_check")
    try:
        version = subprocess.run(["mysql", "-V"], stdout=subprocess.DEVNULL)
        if (version.returncode == 0):
            return True
        else:
            log.km_info("MySQL not installed, falling back to YAML system")
            return False
    except Exception:
        return False

class SQLDriver():
    """This is a wrapper class which provides a slightly nicer API for specific
        MySQL operations:
        - connecting to the database
        - query the database
        - insert into the database
    """

    def __init__(self) -> None:
        self.connection = None

    def try_connect(self) -> None:
        """This method attempts to connect to the database using the data from a
        .env file as the parameters"""
        sql_log = Logger("sql")
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("KM_USER"), password=os.getenv("PASSWORD"))
            # if self.connection.is_connected():
            #   sql_log.km_info("Connected")
        except Error as e:
            sql_log.km_fatal(e)

    def query(self, sql: str, args: tuple):
        """Issue a particular query to the database with optional arguments"""
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor

    def insert(self, sql: str, args: tuple) -> typing.Optional[int]:
        """A wrapper function to take a sql statement string to insert into a
        database"""
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return id

    def fields_from_cursor(cursor) -> typing.Dict:
        """ Given a DB API 2.0 cursor object that has been executed, returns a
        dictionary that maps each field name to a column index; 0 and up. """
        results = {}
        column = 0
        for d in cursor.description:
            results[d[0]] = column
            column = column + 1
        return results

    def fields_from_table_name(self, table_name: str) -> typing.List[str]:
        """A helper function to make getting column names of a specific table
        easier so we can be more dynamic with how we support displaying table
        data
        Example usage:

        driver = SQLDriver()
        driver.try_connect()
        The last line returns a list of all the field names for a table name
        driver.table_fields_from_name(os.getenv("TABLE_NAME"))
        """
        cursor = self.query("SELECT * FROM " + table_name, ())
        field_names = [i[0] for i in cursor.description]
        return field_names
