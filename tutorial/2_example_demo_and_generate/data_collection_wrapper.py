"""
This file implements a wrapper for saving simulation states to disk.
This data collection wrapper is useful for collecting demonstrations.
"""

import os
import time

import numpy as np

from robosuite.utils.mjcf_utils import save_sim_model
from robosuite.wrappers import Wrapper


class DataCollectionWrapper(Wrapper):
    def __init__(self, env, env_interface, directory, collect_freq=1, flush_freq=100):
        """
        Initializes the data collection wrapper.

        Args:
            env (MujocoEnv): The environment to monitor.
            directory (str): Where to store collected data.
            collect_freq (int): How often to save simulation state, in terms of environment steps.
            flush_freq (int): How frequently to dump data to disk, in terms of environment steps.
        """
        super().__init__(env)

        # the base directory for all logging
        self.directory = directory
        self.env_interface = env_interface

        # in-memory cache for simulation states and action info
        self.obs_kwargs = {}
        self.datagen_info = {}
        self.action_infos = []  # stores information about actions taken
        self.successful = False  # stores success state of demonstration

        # how often to save simulation state, in terms of environment steps
        self.collect_freq = collect_freq

        # how frequently to dump data to disk, in terms of environment steps
        self.flush_freq = flush_freq

        if not os.path.exists(directory):
            print("DataCollectionWrapper: making new directory at {}".format(directory))
            os.makedirs(directory)

        # store logging directory for current episode
        self.ep_directory = None

        # remember whether any environment interaction has occurred
        self.has_interaction = False

        # some variables for remembering the current episode's initial state and model xml
        self._current_task_instance_state = None
        self._current_task_instance_xml = None

    def _start_new_episode(self):
        """
        Bookkeeping to do at the start of each new episode.
        """

        # timesteps in current episode
        self.t = 0
        self.has_interaction = False

        # save the task instance (will be saved on the first env interaction)
        self._current_task_instance_xml = self.env.sim.model.get_xml()
        self._current_task_instance_state = np.array(self.env.sim.get_state().flatten())

        # trick for ensuring that we can play MuJoCo demonstrations back
        # deterministically by using the recorded actions open loop
        self.env.reset_from_xml_string(self._current_task_instance_xml)
        self.env.sim.reset()
        self.env.sim.set_state_from_flattened(self._current_task_instance_state)
        self.env.sim.forward()

    def _on_first_interaction(self):
        """
        Bookkeeping for first timestep of episode.
        This function is necessary to make sure that logging only happens after the first
        step call to the simulation, instead of on the reset (people tend to call
        reset more than is necessary in code).

        Raises:
            AssertionError: [Episode path already exists]
        """

        self.has_interaction = True

        # create a directory with a timestamp
        t1, t2 = str(time.time()).split(".")
        self.ep_directory = os.path.join(self.directory, "ep_{}_{}".format(t1, t2))
        assert not os.path.exists(self.ep_directory)
        print("DataCollectionWrapper: making folder at {}".format(self.ep_directory))
        os.makedirs(self.ep_directory)

        # save the model xml
        xml_path = os.path.join(self.ep_directory, "model.xml")
        with open(xml_path, "w") as f:
            f.write(self._current_task_instance_xml)

    def _flush(self):
        """
        Method to flush internal state to disk.
        """
        t1, t2 = str(time.time()).split(".")
        state_path = os.path.join(self.ep_directory, "state_{}_{}.npz".format(t1, t2))
        if hasattr(self.env, "unwrapped"):
            env_name = self.env.unwrapped.__class__.__name__
        else:
            env_name = self.env.__class__.__name__
        np.savez(
            state_path,
            action_infos=self.action_infos,
            successful=self.successful,
            env=env_name,
            initial_state=self.initial_state,
            **self.obs_kwargs,
            **self.datagen_info
        )
        for key in self.obs_kwargs.keys():
            self.obs_kwargs[key] = []
        for key in self.datagen_info.keys():
            self.datagen_info[key] = []
        self.action_infos = []
        self.successful = False

        return state_path

    def reset(self):
        """
        Extends vanilla reset() function call to accommodate data collection

        Returns:
            OrderedDict: Environment observation space after reset occurs
        """
        ret = super().reset()
        self._start_new_episode()
        return ret

    def step(self, action):
        """
        Extends vanilla step() function call to accommodate data collection

        Args:
            action (np.array): Action to take in environment

        Returns:
            4-tuple:

                - (OrderedDict) observations from the environment
                - (float) reward from the environment
                - (bool) whether the current episode is completed or not
                - (dict) misc information
        """
        if not self.has_interaction:
            for key in self.env_interface.get_datagen_info().to_deep_dict()[0].keys():
                self.datagen_info[key] = []
        self.append_datagen_info(action)

        ret = super().step(action)
        self.t += 1

        # on the first time step, make directories for logging
        if not self.has_interaction:
            self._on_first_interaction()
            self.initial_state = self.env.sim.get_state().flatten()
            for key in ret[0].keys():
                self.obs_kwargs[key] = []

        # collect the current simulation state if necessary
        if self.t % self.collect_freq == 0:
            self.append_kwargs_obs(ret[0])
            # self.append_datagen_info(action)

            info = {}
            info["actions"] = np.array(action)
            self.action_infos.append(info)

        # check if the demonstration is successful
        if self.env._check_success():
            self.successful = True

        return ret

    def close(self):
        """
        Override close method in order to flush left over data
        """
        if self.has_interaction:
            path = self._flush()
        self.env.close()

        return path

    def append_kwargs_obs(self, obs_dict):
        for key, value in obs_dict.items():
            self.obs_kwargs[key].append(value)
    
    def append_datagen_info(self, action):
        dic,_,_ = self.env_interface.get_datagen_info(action=action).to_deep_dict()
        for key in self.datagen_info.keys():
            self.datagen_info[key].append(dic[key])
        
