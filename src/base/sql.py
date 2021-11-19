import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


class SQLDriver():
    """This is a wrapper class which provides a slightly nicer API for specific MySQL operations:
        - connecting to the database
        - query the database
        - insert into the database
    """

    def __init__(self):
        self.connection = None
    # This method attempts to connect to the database using the data from a .env file as the parameters

    def try_connect(self):
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"))
            if self.connection.is_connected():
                print("Connected")
        except Error as e:
            print(e)
    # This is a wrapper function to make querying the database slightly nicer

    def query(self, sql, args):
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor
    # This is a wrapper function to make inserting into the database slightly nicer

    def insert(self, sql, args):
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return id

    def fields(cursor):
        """ Given a DB API 2.0 cursor object that has been executed, returns
        a dictionary that maps each field name to a column index; 0 and up. """
        results = {}
        column = 0
        for d in cursor.description:
            results[d[0]] = column
            column = column + 1
        return results
