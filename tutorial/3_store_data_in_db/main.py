"""
This file will show how to store the human demo data in the DB according to the ER diagram in the README.md file.
"""

import mysql.connector as connector
import numpy as np
import re

from tutorial_2_main import tutorial_2



"""
==========================================
Define the utility funcitons to parse an generated trajectory and store it in the DB
==========================================
"""

def parse_and_store_traj(traj, cursor):
    """
    Assume the connection is established and the cursor is created.
    """

    pass

def store_npz_path(npz_path):
    """
    Store the path of the npz file in the DB.
    """

    pass




if __name__ == "__main__":
    

    # Get the file path storing the human demo and the generated trajectory
    path, traj = tutorial_2()

    """
    ==========================================
    Connect to the database and create new DB
    ==========================================
    """

    connection = connector.connect(
        host="localhost",
        user="root")

    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS testRobotDB")
    cursor.execute("USE testRobotDB")

    store_npz_path(path)
    parse_and_store_traj(traj, cursor)

    """
    ==========================================
    TODO: exmaple query to access data from the DB
    ==========================================
    """



    cursor.close()




