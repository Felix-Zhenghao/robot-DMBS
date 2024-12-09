"""
This script only needs to be executed once!!!!!!!!
"""

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

"""
##############################################
# 1. Insert robot into the database
##############################################
"""

insert_robot_query = "INSERT INTO Robots (model, dof, robotType) VALUES (%s, %s, %s)"

for robot_model in ALL_SINGLE_ARM_ROBOTS:
    # Get the DOF from the map or default to something if not found
    dof = DOF_MAP.get(robot_model, 6)  # default 6 DOF if not in map
    cursor.execute(insert_robot_query, (robot_model, dof, 'single_arm'))

"""
##############################################
# 2. Insert demonstrator into the database
##############################################
"""
experience_levels = ['novice', 'intermediate', 'expert']
# Insert ten human demonstrators
for i in range(10):
    cursor.execute("INSERT INTO HumanDemonstrators () VALUES ();")
    cursor.execute("INSERT INTO HumanDemonstrators () VALUES ();")
connection.commit()

# Retrieve the newly inserted demonstrator IDs
cursor.execute("SELECT demonstratorID FROM HumanDemonstrators ORDER BY demonstratorID DESC LIMIT 2;")
demonstrator_ids = [row[0] for row in cursor.fetchall()]

# Generate and insert diverse experience levels for each robot type and demonstrator
for demonstrator_id in demonstrator_ids:
    for robot in ALL_SINGLE_ARM_ROBOTS:
        experience = random.choice(experience_levels)
        cursor.execute(
            "INSERT INTO Experience (robotModel, demonstratorID, experience) VALUES (%s, %s, %s);",
            (robot, demonstrator_id, experience)
        )


"""
##############################################
# 3. Insert objects into the database
##############################################
"""
for obj in OBJECT:
    cursor.execute("INSERT INTO Objects (objectName, classification) VALUES (%s, %s);", (obj, "rigid"))



"""
##############################################
# 4. Insert tasks into the database
##############################################
"""
def json_to_string(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return json.dumps(data)
    
insert_task_query = "INSERT INTO Tasks (taskName, taskDescription, taskSpecification, difficulty, taskType) VALUES (%s, %s, %s, %s, %s)"

for task in TASKS:
    cursor.execute(insert_task_query, (task, TASK_DESCRIPTION_MAP[task], json_to_string(TASK_SPEC_MAP[task]), TASK_DIFFICULTY_MAP[task], TASK_TYPE_MAP[task]))

"""
##############################################
# 5. Insert subtasks into the database
##############################################
"""

insert_subtask_query = "INSERT INTO Subtasks (taskName, subtaskDescription, relativeObject) VALUES (%s, %s, %s)"
for taskname in TASK_TO_SUBTASKS.keys():
    for subtask in TASK_TO_SUBTASKS[taskname]:
        cursor.execute(insert_subtask_query, (taskname, SUBTASK_DESCRIPTION_MAP[subtask], SUBTASK_TO_RELATIVE_OBJECTS[subtask][0]))

cursor.close()
connection.commit()