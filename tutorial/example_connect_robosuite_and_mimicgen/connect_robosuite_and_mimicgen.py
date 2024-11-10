"""
This is a standalone file and can be run directly.
"""

from robosuite.environments.manipulation.nut_assembly import NutAssembly

import mimicgen.utils.robomimic_utils as RobomimicUtils
from robomimic.envs.env_base import EnvType
from mimicgen.env_interfaces.base import make_interface
from mimicgen.env_interfaces.robosuite import RobosuiteInterface

import numpy as np


"""
############################################
First key componenet: the simulation environment
############################################
"""

# register the simulation environment Hello by inheriting from any MujocoEnv
class Hello(NutAssembly):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# set env_meta
# IMPORTANT: args given in create_env() will override the args in env_meta
# for example, if you set has_renderer=False in env_meta, but set has_renderer=True in create_env(),
# the env will have renderer and will render the scene
env_meta = {"env_name": "Hello",
            "type": EnvType.ROBOSUITE_TYPE,
            "env_kwargs": {"robots": "Panda",
                           "has_renderer": False}}
env = RobomimicUtils.create_env(env_meta = env_meta,
                                camera_names=["frontview"],
                                camera_height=84,
                                camera_width=84,
                                use_image_obs=True,
                                use_depth_obs=False,
                                render=True)
print(type(env)) # EnvRobosuite






"""
############################################
Second key componenet: the environment interface
############################################
"""

# register the environment interface Hello by inheriting from RobosuiteInterface
class Hello(RobosuiteInterface):
    """
    Corresponds to robosuite Square task and variants.
    """
    def get_object_poses(self):
        """
        Gets the pose of each object relevant to MimicGen data generation in the current scene.

        Returns:
            object_poses (dict): dictionary that maps object name (str) to object pose matrix (4x4 np.array)
        """

        # two relevant objects - square nut and peg
        return dict(
            square_nut=self.get_object_pose(obj_name=self.env.nuts[self.env.nut_to_id["square"]].root_body, obj_type="body"),
            square_peg=self.get_object_pose(obj_name="peg1", obj_type="body"),
        )

    def get_subtask_term_signals(self):
        """
        Gets a dictionary of binary flags for each subtask in a task. The flag is 1
        when the subtask has been completed and 0 otherwise. MimicGen only uses this
        when parsing source demonstrations at the start of data generation, and it only
        uses the first 0 -> 1 transition in this signal to detect the end of a subtask.

        Returns:
            subtask_term_signals (dict): dictionary that maps subtask name to termination flag (0 or 1)
        """
        signals = dict()

        # first subtask is grasping square nut (motion relative to square nut)
        signals["grasp"] = int(self.env._check_grasp(
            gripper=self.env.robots[0].gripper,
            object_geoms=[g for g in self.env.nuts[self.env.nut_to_id["square"]].contact_geoms])
        )

        # final subtask is inserting square nut onto square peg (motion relative to square peg) - but final subtask signal is not needed
        return signals

# create the environment interface by giving the simulation env: env.base_env
env_interface = make_interface(
    name="Hello",
    interface_type="robosuite",
    env=env.base_env,
)
print(type(env_interface)) # RobosuiteInterface





"""
############################################
Start simulation
############################################
"""
env.reset()
for i in range(100):
    result = env.step(np.random.randn(8))
    env.render(mode='human',camera_name='frontview')

    # this is a unique method of EnvRobosuite
    # if directly use NutAssembly, this method is not available
    # methods like this will be used in MimicGen data generation loop
    # so initialize the env with RobomimicUtils.create_env() is essential
    print(env.get_observation())

    # this is a unique method of RobosuiteInterface
    # we need the environment interface to get information for data generation
    print(env_interface.get_datagen_info().eef_pose)
