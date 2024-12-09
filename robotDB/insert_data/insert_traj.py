import random
import json

import mysql.connector as connector
import numpy as np

from constants import *

import sys
sys.path.append('/Users/chizhenghao/Desktop/uchicago/24 fall/databases/db-pj/robotDB/')
print(sys.path)

connection = connector.connect(
    host="localhost",
    user="root")

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS RobotDB")
cursor.execute("USE RobotDB")

"""
##############################################
# 1. Insert trajectories into the database
##############################################
"""
from backend import render_env, get_env_interface, teleoperate

def teleoperate_and_store(taskname: str,
                          demonstrator_id: int,
                          robot_model: str,):

    assert taskname in TASKS_MAP.keys(), f"Task {taskname} not found in TASKS_MAP."

    # randomly choose a task variant
    env_name = random.choice(TASKS_MAP[taskname])
    
    # query and get task_spec
    cursor.execute("SELECT taskSpecification FROM Tasks WHERE taskName = %s;", (taskname,))
    task_spec = json.loads(cursor.fetchone()[0])

    # get env and env interface
    env = render_env(env_name=env_name,
                     robot_type=robot_model,
                     render=False)
    env_interface = get_env_interface(env=env)

    # teleoperate
    state_path, obs_key, datagen_key = teleoperate(env, env_interface)

    # process the keys: merge keys into a single string split with '*/*'
    obs_key_str = "*/*".join(obs_key)
    datagen_key_str = "*/*".join(datagen_key)

    # insert the trajectory into the database
    cursor.execute("INSERT INTO Demonstrations (trainingDataKey, dataGenKey, filePathNPZ, demonstratorID, robotModel, taskName, success, label) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                   (obs_key_str, datagen_key_str, state_path, demonstrator_id, robot_model, taskname, 1, "source_demo"))
    
    connection.commit()

    print("================ Successfully generated and stored a trajectory ================")
    
    return state_path

# teleoperate_and_store("Square", 1, "UR5e")



"""
##############################################
# 2. Get traj from the database, generate, and store
##############################################
"""

# now, data path, robot type, and task spec has be feteched
# just wrap generate_traj in backend.py
from typing import List, Dict
from backend import generate_traj

def gen_and_store(demonstrator_id: int, # same as the source demo used
                  robot_type: str,
                  dataset_path: str,
                  task_spec: List[Dict]) -> str:
    
    dic = np.load(dataset_path, allow_pickle=True)
    env_name = dic["env"].item()
    taskname = env_name.split("_")[0]

    state_path, obs_key, datagen_key, success = generate_traj(env_name, robot_type, dataset_path, task_spec)
    obs_key_str = "*/*".join(obs_key)
    datagen_key_str = "*/*".join(datagen_key)

    cursor.execute("INSERT INTO Demonstrations (trainingDataKey, dataGenKey, filePathNPZ, demonstratorID, robotModel, taskName, success, label) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                   (obs_key_str, datagen_key_str, state_path, demonstrator_id, robot_type, taskname, success, "robot_generated"))


    connection.commit()

    print("================ Successfully generated and stored a trajectory ================")


"""
Teleoperate and store 20 trajectories with random task and embodiment
"""
# for i in range(1):

#     # randomly choose from [1,2]
#     demonstrator_id = random.choice([1, 2])
#     robot_type = random.choice(ALL_SINGLE_ARM_ROBOTS)
#     taskname = random.choice(TASKS)

#     print(robot_type, taskname)

#     teleoperate_and_store(taskname="Kitchen",
#                           demonstrator_id=demonstrator_id,
#                           robot_model="Panda")

"""
Generate 10 trajectories
"""

# for i in range(1):
#     # randomly select on entry of Demonstrations with label "source_demo"
#     cursor.execute("SELECT * FROM Demonstrations WHERE label = 'source_demo' ORDER BY RAND() LIMIT 1;")
#     row = cursor.fetchone()
    
#     dataset_path = row[4]
#     demonstrator_id = row[5]
#     robot_type = row[6]
#     taskname = row[7]

#     # get task spec
#     cursor.execute("SELECT taskSpecification FROM Tasks WHERE taskName = %s;", (taskname,))
#     task_spec = json.loads(cursor.fetchone()[0])

#     print(dataset_path, demonstrator_id, robot_type, taskname)
#     print(task_spec)
#     try:
#         gen_and_store(demonstrator_id=demonstrator_id,
#                       robot_type=robot_type,
#                       dataset_path=dataset_path,
#                       task_spec=task_spec)
#     except Exception as e:
#         # if the trajectory generation fails, print the error and continue
#         continue

from backend import replay_episode
replay_episode("npz_data/ep_1733777696_438442/state_1733777785_1731682.npz", "Panda")