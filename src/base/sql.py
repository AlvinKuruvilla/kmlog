import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from base.log import Logger
from typing import Optional
import os


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
                host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"))
            # if self.connection.is_connected():
            #   sql_log.km_info("Connected")
        except Error as e:
            sql_log.km_fatal(e)
    # This is a wrapper function to make querying the database slightly nicer

    def query(self, sql: str, args: tuple):
        """Issue a particular query to the database with optional arguments"""
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor

    def insert(self, sql: str, args: tuple) -> Optional[int]:
        """A wrapper function to take a sql statement string to insert into a
        database"""
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return id

    def fields(cursor) -> dict:
        """ Given a DB API 2.0 cursor object that has been executed, returns a
        dictionary that maps each field name to a column index; 0 and up. """
        results = {}
        column = 0
        for d in cursor.description:
            results[d[0]] = column
            column = column + 1
        return results
