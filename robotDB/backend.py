import os
import json
from typing import Dict, Any, List, Tuple, Union

import numpy as np

# import utilities from mimicgen
from mimicgen.env_interfaces.base import make_interface
from mimicgen.env_interfaces.robosuite import RobosuiteInterface

# import environments defined in mimicgen
from mimicgen.envs.robosuite.coffee import Coffee_D0, Coffee_D1, Coffee_D2, CoffeePreparation_D0, CoffeePreparation_D1
from mimicgen.envs.robosuite.hammer_cleanup import HammerCleanup_D0, HammerCleanup_D1
from mimicgen.envs.robosuite.kitchen import Kitchen_D0, Kitchen_D1
from mimicgen.envs.robosuite.mug_cleanup import MugCleanup_D0, MugCleanup_D1
from mimicgen.envs.robosuite.nut_assembly import Square_D0, Square_D1, Square_D2
from mimicgen.envs.robosuite.pick_place import PickPlace_D0
from mimicgen.envs.robosuite.stack import Stack_D0, Stack_D1, StackThree_D0, StackThree_D1
from mimicgen.envs.robosuite.threading import Threading_D0, Threading_D1, Threading_D2

# import robomimic utils to create environment
import mimicgen.utils.robomimic_utils as RobomimicUtils
from robomimic.envs.env_base import EnvType
from robomimic.envs.env_robosuite import EnvRobosuite

# get namelists
from robosuite.environments.base import REGISTERED_ENVS
from robosuite import load_controller_config
from mimicgen.env_interfaces.base import REGISTERED_ENV_INTERFACES

ALL_ENVIRONMENTS = list(REGISTERED_ENVS.keys())
ALL_SINGLE_ARM_ROBOTS = ["Panda", "Sawyer", "IIWA", "UR5e", "Jaco", "Kinova3"]
ALL_ENV_INTERFACE = list(REGISTERED_ENV_INTERFACES['robosuite'].keys())


"""
##########################################################
# Function 1: create an environment and render
##########################################################
"""
def render_env(env_name: str,
               robot_type: str,
               render: bool = True) -> EnvRobosuite:
    """
    Render the environment with the given name and robot type.

    :param env_name: The name of the environment.
    :param robot_type: The type of the robot.
    :param render: Whether to render the environment.
    :return: The created environment.
    """
    
    assert env_name in ALL_ENVIRONMENTS, f"Invalid environment name: {env_name}"
    assert robot_type in ALL_SINGLE_ARM_ROBOTS, f"Invalid robot type: {robot_type}"

    env_meta = {"env_name": env_name,
                "type": EnvType.ROBOSUITE_TYPE,
                "env_kwargs": {"robots": robot_type,
                               "has_renderer": False,
                               "controller_configs": load_controller_config(default_controller="OSC_POSE")}}
    
    env = RobomimicUtils.create_env(env_meta = env_meta,
                                    camera_names=["frontview","agentview"],
                                    camera_height=128,
                                    camera_width=128,
                                    use_image_obs=True,
                                    use_depth_obs=False,
                                    render=True)
    # render the environment
    env.reset()

    if render:
        action_dim = env.action_dimension
        for _ in range(100):
            action = np.random.randn(action_dim)
            env.step(action)
            env.render(mode='human',camera_name='frontview')

    return env

# render_env('Kitchen_D1', 'Sawyer')


"""
##########################################################
# Function 2: teleoperate a trajectory
##########################################################
"""
def get_env_interface(env: EnvRobosuite,) -> RobosuiteInterface:
    # get interface_name by turning *_D1 to MG_*
    env_name = env.name
    task_name = env_name.split('_')[0]
    interface_name = 'MG_' + task_name
    assert interface_name in ALL_ENV_INTERFACE, f"Invalid environment interface name: {interface_name}"

    # create the environment interface
    env_interface = make_interface(name=interface_name,
                                   interface_type='robosuite',
                                   env=env.base_env)
    
    return env_interface


def teleoperate(env: EnvRobosuite,
                env_interface: RobosuiteInterface,
                ) -> Tuple[str, List[str], List[str]]:
    """
    Teleoperate the robot to collect a single human demonstration.

    :param env: The environment to teleoperate.
    :return: The path to the generated trajectory, the observation keys, and the data generation keys.
    """

    # include the path to the generation_util folder
    import sys
    sys.path.append('robotDB/generation_util')

    # import stuff needed for data generation
    from robosuite.wrappers import VisualizationWrapper
    from robosuite.devices import Keyboard
    from generation_util.collect_human_demonstration import collect_human_trajectory
    from generation_util.data_collection_wrapper import DataCollectionWrapper
    from generation_util.data_generator import DataGenerator
    
    # collect the human demonstration
    demo_env = VisualizationWrapper(env.env)
    demo_env = DataCollectionWrapper(demo_env, env_interface, directory="npz_data/")
    device = Keyboard(pos_sensitivity=1., rot_sensitivity=1.)
    state_path, obs_key, datagen_key, _ = collect_human_trajectory(demo_env, device, "right", "single-arm-opposed")

    print(f"State path: {state_path}")
    print(f"Obs key: {obs_key}")
    print(f"Datagen key: {datagen_key}")
    return state_path, obs_key, datagen_key

# env = render_env('Square_D0', 'UR5e', False)
# teleoperate(env, get_env_interface(env))

"""
##########################################################
# Function 3: Store the generated trajectory into DB
##########################################################
"""

taskname = 'square'
dataset_path = 'ep_1733617052_226272/state_1733617079_609206.npz'
with open(f'robotDB/taskspecs/{taskname}.json') as f:
    task_spec = json.load(f)

def convert_traj_to_npz(env_name: str,
                        traj: Dict[str, Union[np.ndarray, bool, list]]
                        ) -> np.ndarray:
    import time

    # deal with observations
    observations = {}
    for key in traj['observations'][0].keys():
        observations[key] = []
    for obs in traj['observations']:
        for key in observations.keys():
            observations[key].append(obs[key])

    datagen_infos = {}
    for key in traj['datagen_infos'][0].to_deep_dict()[0].keys():
        datagen_infos[key] = []

    def append_datagen_info(datagen_info,
                            datagen_infos,):
        dic,_,_ = datagen_info.to_deep_dict()
        for key in datagen_infos.keys():
            datagen_infos[key].append(dic[key])
    
    # deal with datagen infos
    for datagen_info in traj['datagen_infos']:
        append_datagen_info(datagen_info, datagen_infos)


    t1, t2 = str(time.time()).split(".")
    state_path = os.path.join('npz_data/', "state_{}_{}.npz".format(t1, t2))
    np.savez(
        state_path,
        action_infos=traj['actions'],
        successful=traj['success'],
        env=env_name,
        **observations,
        **datagen_infos
    )

    return state_path, list(observations.keys()), list(datagen_infos.keys()), traj['success']

def generate_traj(env_name: str,
                  robot_type: str,
                  dataset_path: str,
                  task_spec: List[Dict]) -> str:
        
    import sys
    sys.path.append('robotDB/generation_util')
    from generation_util.data_generator import DataGenerator

    generator = DataGenerator(task_spec=task_spec,
                              dataset_path=dataset_path,)

    env = render_env(env_name=env_name,
                     robot_type=robot_type,
                     render=False)
    env_interface = get_env_interface(env)
    generated_traj = generator.generate(env=env,
                                        env_interface=env_interface,
                                        camera_names=["agentview"],
                                        render=True)
    # print(generated_traj['observations'])
    # print(len(generated_traj['observations'])) # len(traj)
    # print(type(generated_traj['observations'])) # 'list'
    return convert_traj_to_npz(env_name, generated_traj)

# task_spec = json.load(open('robotDB/taskspecs/Square.json'))
# print(generate_traj('Square_D0', 'UR5e', "npz_data/ep_1733709720_6746821/state_1733709764_120378.npz", task_spec))

"""
##########################################################
# Function 4: Replay a source demo
##########################################################
"""

def replay_episode(npz_file_path: str,
                   robot_type: str,):

    dic = np.load(npz_file_path, allow_pickle=True)
    env_name = dic["env"].item()
    env = render_env(env_name=env_name,
                     robot_type=robot_type,
                     render=False)

    env.base_env.sim.set_state_from_flattened(dic["initial_state"])

    actions = dic["action_infos"]
    for action in actions:
        env.step(action["actions"])
        env.render()

    env.close()

    print("====================== Replay successful ======================")
