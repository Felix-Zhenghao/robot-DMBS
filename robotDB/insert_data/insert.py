import random
import json

import mysql.connector as connector
import numpy as np

from constants import *

connection = connector.connect(
    host="localhost",
    user="root")


cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS RobotDB")
cursor.execute("USE RobotDB")



experience_levels = ['novice', 'intermediate', 'expert']
# Generate and insert diverse experience levels for each robot type and demonstrator
for demonstrator_id in range(3,19):
    for robot in ALL_SINGLE_ARM_ROBOTS:
        experience = random.choice(experience_levels)
        cursor.execute(
            "INSERT INTO Experience (robotModel, demonstratorID, experience) VALUES (%s, %s, %s);",
            (robot, demonstrator_id, experience)
        )

connection.commit()