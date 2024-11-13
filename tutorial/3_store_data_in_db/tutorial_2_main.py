from mimicgen.env_interfaces.robosuite import RobosuiteInterface
from mimicgen.datagen.data_generator import DataGenerator

from robosuite.environments.manipulation.nut_assembly import NutAssembly
from mimicgen.envs.robosuite.nut_assembly import Square_D1
import mimicgen.utils.robomimic_utils as RobomimicUtils
from robomimic.envs.env_base import EnvType
from robosuite import load_controller_config

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay",
        type=bool,
        default=False,
        help="Whether to replay the demonstration trajectory. \
              If True, collect+replay+generate will be executed. \
              If False, only collect+generate will be executed.",
    )
    args = parser.parse_args()

    """
    ############################################
    STEP 1: Define task specification
    ############################################
    """
    def tutorial_2():
        """
        Start this tutorial and return the generated trajectory.
        """

        task_spec = [
            {
                "object_ref": "square_nut",
                "subtask_term_signal": "grasp",
                "subtask_term_offset_range": [
                    10,
                    20
                ],
                "selection_strategy": "nearest_neighbor_object",
                "selection_strategy_kwargs": {
                    "nn_k": 3
                },
                "action_noise": 0.05,
                "num_interpolation_steps": 5,
                "num_fixed_steps": 0,
                "apply_noise_during_interpolation": False
            },
            {
                "object_ref": "square_peg",
                "subtask_term_signal": None,
                "subtask_term_offset_range": [
                    0,
                    0
                ],
                "selection_strategy": "nearest_neighbor_object",
                "selection_strategy_kwargs": {
                    "nn_k": 3
                },
                "action_noise": 0.05,
                "num_interpolation_steps": 5,
                "num_fixed_steps": 0,
                "apply_noise_during_interpolation": False
            }
        ]


        """
        ############################################
        STEP 2: Create the environment class and meta for the task
        ############################################
        """
        # register the environment Hello by inheriting from any MujocoEnv
        class Hello(Square_D1):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        # set env_meta
        # IMPORTANT: args given in create_env() will override the args in env_meta
        # for example, if you set has_renderer=False in env_meta, but set has_renderer=True in create_env(),
        # the env will have renderer and will render the scene
        env_meta = {"env_name": "Hello",
                    "type": EnvType.ROBOSUITE_TYPE,
                    "env_kwargs": {"robots": "Panda",
                                "has_renderer": True,
                                "controller_configs": load_controller_config(default_controller="OSC_POSE")}}

        env = RobomimicUtils.create_env(env_meta = env_meta,
                                        camera_names=["frontview"],
                                        camera_height=84,
                                        camera_width=84,
                                        use_image_obs=True,
                                        use_depth_obs=False,
                                        render=True,
                                        render_offscreen=True)



        """
        ############################################
        STEP 3: Create the environment interface for the task
        ############################################
        """
        from mimicgen.env_interfaces.base import make_interface

        # register the environment Hello by inheriting from any MujocoEnv
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

        env_interface = make_interface(name="Hello",
                                    env=env.base_env,
                                    interface_type="robosuite")



        """
        ############################################
        STEP 4: Generate source human demo by creating human demo env
        ############################################
        """
        from data_collection_wrapper import DataCollectionWrapper
        from collect_human_demonstration import collect_human_trajectory
        from robosuite.wrappers import VisualizationWrapper
        from robosuite.devices import Keyboard

        # Grab reference to controller config and convert it to json-encoded string
        config = {
            "env_name": env_meta["env_name"],
            "robots": env_meta["env_kwargs"]["robots"],
            "controller_configs": load_controller_config(default_controller="OSC_POSE"),
        }

        demo_env = VisualizationWrapper(env.env)

        # wrap the environment with data collection wrapper
        demo_env = DataCollectionWrapper(demo_env, env_interface, directory=".")

        device = Keyboard(pos_sensitivity=1., rot_sensitivity=1.)

        # comment out because it should be executed in `__main__` mode
        state_path = collect_human_trajectory(demo_env, device, "Panda", "single-arm-opposed")


        """
        ############################################
        STEP 5: Generate data
        ############################################
        """
        from data_generator import DataGenerator

        # comment out because it should be executed in `__main__` mode

        generator = DataGenerator(task_spec=task_spec,
                                dataset_path=state_path,
                                demo_keys=["one_demo"])

        generated_traj = generator.generate(env=env,
                        env_interface=env_interface,
                        camera_names=["agentview"],
                        render=True)
    
        return state_path, generated_traj