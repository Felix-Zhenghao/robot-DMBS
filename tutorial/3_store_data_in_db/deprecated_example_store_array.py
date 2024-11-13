"""
This file is deprecated. Please see main.py for the latest version.
"""

import pymysql.cursors
import numpy as np
import re

x = np.random.rand(5, 3, 3)

# connect to the local MySQL
connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             database = None,
                             cursorclass = pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS testdb") # create testdb dataset
        cursor.execute("USE testdb")
    connection.commit()

    with connection.cursor() as cursor:
        # create relation, array has type BLOB
        cursor.execute("CREATE TABLE IF NOT EXISTS NumpyTest (testID INT, array BLOB, shape0 INT, shape1 INT)")
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO NumpyTest (testID, array, shape0, shape1) VALUES (1, %s, {x.shape[0]}, {x.shape[1]})", (x,)) # store array
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM NumpyTest")
        result = cursor.fetchall()
    connection.commit()


array = result[-1]['array'].decode('utf-8')
array = ' '.join(re.findall(r'\d+\.\d+', array))
print(np.fromstring(array, sep=' ').reshape(result[-1]['shape0'], result[-1]['shape1'])) # retrieve array