# DOC VERSION 2.0
This tutorial is used the show the whole pipeline of:
- Collecting demonstration data through human teleoperation
- Generate data according to the human demonstration just created

You can directly run `main.py` to undergo these two things:
- Teleoperate the robot (see [here](https://robosuite.ai/docs/algorithms/demonstrations.html#keyboard-controls) to understand how to control the robot using the keyboard)
- Generate data from your demonstation. **The generation process will be rendered so that you can the generation process** :)

Let's go through the whole pipeline step by step.

# Step 1: Define the task specification 
The task specification is used to tell the data generation system how split the subtask and how to figure out the termination of a subtask. For every task, you should define a task specification. See [here](https://mimicgen.github.io/docs/tutorials/datagen_custom.html#step-2-implement-task-specific-config) for more information.


# Step 2: Create the simulation environment for the task
This can be split into three sub-steps:
- 2.1 Define the task-specific and register by inheriting from `MujocoEnv`.
- 2.2 Define the env_meta to send parameters when launching the environment.
- 2.3 Launch (create) the simulation environment by calling `RobomimicUtils.create_env()`.

You can take a look at `tutorial/1_example_connect_robosuite_and_mimicgen`. Pay attention, env_kwargs is the place you can send any parameters to the environment launcher. The underlying code that `create_env()` calls is `robosuite.make(env_kwargs \union some_other_args)`, so you can think of `env_kwargs` is just sending parameters to `robosuite.make()`. For instance, in the code of this tutorial, the `env_kwargs` is as follows. For instance, the last para tells robosuite that the controller used by the robot is "OSC_POSE".
```python
"env_kwargs": {"robots": "Panda",
                "has_renderer": Ture,
                "controller_configs": load_controller_config(default_controller="OSC_POSE")}
```

# Step 3: Create the environment interface for the task
Also, see `tutorial/1_example_connect_robosuite_and_mimicgen` for more information.

Now we state the relationship between step 2 and step 3 as follows:
- Step 2 is used to create the simulation env, this is the env that the simulation engine actually runs.
- Step 3 takes the environment created in step 2, and add some methods (interfaces) to enable easier query for information needed to generate data.

Again, environment and environment interface are two key components to generate data using MimicGen.


# Step 4: Collect human demonstration
Except for the `main.py`, pay attention to the following file:
- `data_collection_wrapper.py` defines a wrapper class to wrap the simulation environment. The main purpose of this is to store necessary data during demonstration.
- `collect_human_demonstration.py` contains the function `collect_human_trajectory`. This is the function called to launch the demonstration process and store the data during demonstration.
- `replay.py` is used to replay the demonstration.

There are several topics worth discussion. See as follows.

## Topic 1: Data flushing
All data needed is flushed to the disk in a single `.npz` file. `.npz` file can be think of a dictionary of `np.ndarray`.

**Here, for simplicity, we directly flush all observation data. This will make the code much cleaner. Another modification compared with the robosuite codebase is we choose to flush data once for one demo. This will cause more RAM demand during data collection.**

If you are interested in the original implementation of data flushing, see here:

> The data flushing code is [here](https://github.com/Felix-Zhenghao/robosuite/blob/master/robosuite/wrappers/data_collection_wrapper.py#L119-L138). Also pay attention that there will be mutiple files flushed because there's a [flush_frequency](https://github.com/Felix-Zhenghao/robosuite/blob/master/robosuite/wrappers/data_collection_wrapper.py#L193-L194). If we want to store data per-frame, then use `flush_freq=1`; if we want to store per-demo, then make `flush_freq` very big. Pay attention that if the task is too long-horizon, we may run out of RAM if we flush once per demo!!! We only need to modify `_flush()` and `flush_freq`, and we can have our data organized in the database!
> Note that the state data is [flattened](https://github.com/Felix-Zhenghao/robosuite/blob/master/robosuite/wrappers/data_collection_wrapper.py#L175). Only position, velocity is in the state data. To convert state data into, say, camera observation, robomimic will replay the episode according to state. There is a trade-off here: if we only store state data, we will have less I/O overhead when reading data and less disk storage and RAM demand, but we will need more compute to restore other observation. Else, if we store the whole `OrderedDict` the env returns, we will use less compute but more disk storage space, RAM and I/O overhead.

The keys of the example task (keys of the `.npz` file if you run this example) is:
```
['action_infos', 'successful', 'env', 'initial_state', 'robot0_joint_pos', 
 'robot0_joint_pos_cos', 'robot0_joint_pos_sin',
 'robot0_joint_vel', 'robot0_eef_pos', 'robot0_eef_quat', 'robot0_eef_vel_lin', 
 'robot0_eef_vel_ang', 'robot0_gripper_qpos', 'robot0_gripper_qvel', 'frontview_image', 
 'SquareNut_pos', 'SquareNut_quat', 'SquareNut_to_robot0_eef_pos', 'SquareNut_to_robot0_eef_quat', 
 'peg1_pos', 'robot0_proprio-state', 'object-state', 'eef_pose', 'square_nut', 
 'square_peg', 'grasp', 'target_pose', 'gripper_action']
```

The data is recorded per-frame, which mean that things (except for `initial_state`) has shape `(T, ...)` where T is the number timesteps of the demonstration.

The information can be split into three classes:
- Information needed for data generation, like `square_nut`, which is the pose of the nut object in the simulation. 
- Information needed for training, like `frontview_image`, which is a third-view image observation.
- Information needed both for training and data generation, like `action_infos`, which is the action take at each timestep.

Some play the important role are introduced here:
- `initial_state`. If you want to replay any demonstration, the first thing is to recover the initial state before any action is taken in the environment. This is used to store the initial state of the environment.
- `action_infos`. This is just the action taken by the robot (from the demonstration) each step during the simulation.
- `target_pose`, `eef_pose`, `gripper_action`, `square_nut`, etc. These are keys of `DatagenInfo` class. This is the class who record the information needed for data generation for each env.step(). In the other word, this data is used for data generation.


## Topic 2: Replay episode
To replay the episode you collected, please directly run `main.py` by giving argument `--replay True`.

The replay can be split into following steps:
- create an identical environment as where the demo happened
- set the env state to the initial state of the demo
- feed demo actions and step the environment

`replay.py` will also save the video record of the replay as `assets/video.mp4`.

# Step 5: Data generation

The crux of data generation is to get the correct `DatagenInfo` from the source demonstration. It also needs task specification and environment interface. You should read through these chapters of MimicGen doc:
- [DatagenInfo](https://mimicgen.github.io/docs/modules/datagen.html#datagen-info)
- [Task-specific env interface](https://mimicgen.github.io/docs/tutorials/datagen_custom.html#step-1-implement-task-specific-environment-interface)
- [Task_specific config](https://mimicgen.github.io/docs/tutorials/datagen_custom.html#step-1-implement-task-specific-environment-interface)
- [Env interfaces](https://mimicgen.github.io/docs/tutorials/datagen_custom.html#step-1-implement-task-specific-environment-interface)

I strongly recommend you to read through `tutorial/2_example_demo_and_generate/data_generator.py` and try to understand how data is generated given an `.npz` file by printing out intermediate contents.


# Bonus
If you want to try a more complex task, run `main_kitchen.py`. The task description is here:
> Switch stove on, place pot onto stove, place bread into pot, place pot in front of serving region and push it there, and turn off the stove.