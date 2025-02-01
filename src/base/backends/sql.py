# pylint: disable=C0301
# pylint: disable=E0401
# pylint: disable=W0703
# pylint: disable=E0401
# pylint: disable=C0103
# pylint: disable=C0114

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import typing
import os
import subprocess
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
from base.log import Logger


def check_mysql_installed_and_env_configured_correctly() -> bool:
    """
    Check if mysql is installed on the system and check if any of the required .env fields are missing

    Parameters
    ----------
    None

    Returns
    ----------
    bool
        If True, then mysql is installed in the system and .env file has all the necessary fields.
        If False then mysql is not installed and/or .env file doesn't have all the necessary fields to work with the database.
    """
    # TODO: check if there needs to be a different way to do this on Windows
    try:
        version = subprocess.run(["mysql", "-V"], stdout=subprocess.DEVNULL, check=True)
        c = []
        config = dotenv_values(".env")
        for k in config.keys():
            c.append(k)
        if not "KM_USER" in c or not "PASSWORD" in c or not "DB_HOST" in c or not "DB_NAME" in c or not "TABLE" in c:
            return False
        return bool(bool(version.returncode == 0) and (not len(c) == 0))
    except Exception:
        return False


# TODO: Add an extra check if the tables are properly setup


def fields_from_cursor(cursor) -> typing.Dict:
    """
    Given a DB API 2.0 cursor object that has been executed, returns a
    dictionary that maps each field name to a column index; 0 and up.

    Parameters
    ----------
    Cursor object

    Returns
    ----------
    dict
        The dictionary mapping from field names to column indexes
    """
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results


class SQLDriver:
    """This is a wrapper class which provides a slightly nicer API for specific
    MySQL operations:
    - connecting to the database
    - query the database
    - insert into the database
    """

    def __init__(self) -> None:
        self.connection = None

    def try_connect(self) -> None:
        """
        This method attempts to connect to the database using the data from a
        .env file as the parameters

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        sql_log = Logger()
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("KM_USER"),
                password=os.getenv("PASSWORD"),
            )
            # if self.connection.is_connected():
            #   sql_log.km_info("Connected")
        except Error as e:
            sql_log.km_fatal(e)

    def query(self, sql: str, args: tuple):
        """
        Issue a particular query to the database with optional arguments

        Parameters
        ----------
        str:
            The sql query, as a string to be executed
            This query can also be filled in with prepared arguments
        tuple:
            A tuple of arguments to be passed to the sql statement
            for prepared statements
        Returns
        ----------
        Cursor
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor

    def insert(self, sql: str, args: tuple) -> typing.Optional[int]:
        """
        Insert into a database through the SQL statement

        Parameters
        ----------
        str:
            The sql query, as a string to be executed
            This query can also be filled in with prepared arguments
        tuple:
            A tuple of arguments to be passed to the sql statement
            for prepared statements
        Returns
        ----------
        typing.Optional[int]
            The row of the inserted data, if the insert was successful
        """
        cursor = self.query(sql, args)
        row_id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return row_id

    def fields_from_table_name(self, table_name: str) -> typing.List[str]:
        """
        A helper function to make getting column names of a specific table
        easier so we can be more dynamic with how we support displaying table
        data

        Parameters
        ----------
        str:
            The sql query, as a string to be executed
            This query can also be filled in with prepared arguments
        tuple:
            A tuple of arguments to be passed to the sql statement
            for prepared statements
        Returns
        ----------
        typing.Optional[list]
            A list of the names of the columns of a table, if successful

        Example
        --------
        driver = SQLDriver()
        driver.try_connect()
        The last line returns a list of all the field names for a table name
        driver.table_fields_from_name(os.getenv("TABLE_NAME"))
        """
        cursor = self.query("SELECT * FROM " + table_name, ())
        field_names = [i[0] for i in cursor.description]
        return field_names
